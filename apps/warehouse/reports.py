from django.db.models import Count
from apps.warehouse.models import StockMove
from apps.warehouse.models import Product

# ----------------- REPORT STOCK MOVE MODEL -------------- #


def report_move(request):

    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    report_type = request.POST.get('report_type', '')
    if report_type == 'by_move':
        sql = \
            '''
            SELECT  distinct sm.id as id,  sm.code, sl.name AS location,
            sld.name AS location_dest , p.name AS product,
            pu.name AS unit, pp.code AS package,
            sm.quantity AS quantity, sm.pieces AS pieces,
            mu.abbreviation AS measure,
            sm.move_type AS move_type,
            to_char(sm.date, 'DD-MM-YYYY') AS date,
            cu.first_name || ' ' || cu.last_name AS user

            FROM stock_move sm

            LEFT JOIN stock_location sl ON sl.id = sm.location_id_id
            LEFT JOIN stock_location sld ON sld.id = sm.location_dest_id_id
            LEFT JOIN product_unit pu ON pu.id = sm.unit_id_id
            LEFT JOIN product_package pp ON  pp.id = sm.package_id_id
            LEFT JOIN product p ON (
                p.id = pu.product_id_id OR p.id  = pp.product_id_id)
            LEFT JOIN measurement_unit mu ON mu.id = p.measure_id_id
            LEFT JOIN core_user cu ON cu.id = sm.user_creator_id

            WHERE  sm.date BETWEEN '%s'  AND '%s'

            ''' % (start_date, end_date)

        for move in StockMove.objects.raw(sql):
            item = move.unit if move.unit \
                else move.package
            quantitys = move.quantity if move.unit \
                else move.pieces
            data.append([
                move.code, move.location,
                move.location_dest,
                move.product, item,
                str(quantitys) + ' ' + move.measure,
                move.move_type,
                move.date,
                move.user_creator.first_name + ' ' +
                move.user_creator.last_name,
            ])

    if report_type == 'by_product':
        sql = \
            '''
            SELECT p.id as id, p.name,
            (SUM(sm.quantity) || ' ' || mu.abbreviation) AS quantity,
            SUM(sm.pieces) AS pieces

            FROM product p

            LEFT JOIN measurement_unit mu ON mu.id = p.measure_id_id
            LEFT JOIN product_unit pu ON pu.product_id_id = p.id
            LEFT JOIN product_package pp ON pp.product_id_id = p.id
            LEFT JOIN stock_move sm ON (
                sm.unit_id_id = pu.id OR sm.package_id_id = pp.id)

            WHERE  sm.date BETWEEN '%s'  AND '%s' AND (
            sm.quantity > 0 OR sm.pieces > 0)

            GROUP BY p.name, p.id, mu.abbreviation
            ''' % (start_date, end_date)

        for product in Product.objects.raw(sql):
            data.append([
                product.name,
                product.quantity,
                product.pieces,
            ])

    if report_type == 'by_location':
        sql = \
            '''
            SELECT sl.id as id, sl.name,
            (SUM(sm.quantity) || ' ' || mu.abbreviation) AS quantity,
            SUM(sm.pieces) AS pieces

            FROM stock_move sm

            LEFT JOIN stock_location sl ON sl.id = sm.location_dest_id_id
            LEFT JOIN product_unit pu ON pu.id = sm.unit_id_id
            LEFT JOIN product_package pp ON  pp.id = sm.package_id_id
            LEFT JOIN product p ON (
                p.id = pu.product_id_id OR p.id  = pp.product_id_id)
            LEFT JOIN measurement_unit mu ON mu.id = p.measure_id_id

            WHERE  sm.date BETWEEN '%s'  AND '%s' AND (
                sm.quantity > 0 OR sm.pieces > 0)

            GROUP BY sl.id, mu.abbreviation, sl.name
            ''' % (start_date, end_date)

        for location in StockMove.objects.raw(sql):
            data.append([
                location.name,
                location.quantity,
                location.pieces,
            ])

    if report_type == 'by_user':
        sql = \
            '''
            SELECT distinct cu.id as id,
            cu.first_name || ' ' || cu.last_name AS user,
            (SUM(sm.quantity) || ' ' || mu.abbreviation) AS quantity,
            SUM(sm.pieces) AS pieces

            FROM stock_move sm

            LEFT JOIN core_user cu ON cu.id = sm.user_creator_id
            LEFT JOIN product_unit pu ON pu.id = sm.unit_id_id
            LEFT JOIN product_package pp ON  pp.id = sm.package_id_id
            LEFT JOIN product p ON (
                p.id = pu.product_id_id OR p.id  = pp.product_id_id)
            LEFT JOIN measurement_unit mu ON mu.id = p.measure_id_id
            WHERE  sm.date BETWEEN '%s'  AND '%s' AND (
                sm.quantity > 0 OR sm.pieces > 0)

            GROUP BY cu.id, mu.abbreviation
            ''' % (start_date, end_date)

        for user in StockMove.objects.raw(sql):
            data.append([
                user.user,
                user.quantity,
                user.pieces,
            ])

    return data
