from django.contrib import messages
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import StockControl
from apps.warehouse import functions


def validate_moves(request, move):
    '''
    Diferentes validaciones previas a la creación del movimiento
    Si ocurre algún error en las validaciones,
    se agrega el mensaje de error a la lista 'errors'
    Finalmente la función devuelve la lista 'errors'
    '''
    
    if move.unit_id:
        if move.unit_id.product_id.measure_id:
            measure = move.unit_id.product_id.measure_id.abbreviation
        else:
            measure = ' '
        item_move = move.unit_id

    elif move.package_id:
        if move.package_id.product_id.measure_id:
            measure = move.package_id.product_id.measure_id.abbreviation
        else:
            measure = ' '
        item_move = move.package_id

    __VALID_MOVES__ = [
        'Ingress-Internal',
        'Internal-Internal',
        'Internal-Egress',
    ]

    __MOVE_TYPE__ = {
        'Ingress-Internal': 'Ingress',
        'Internal-Internal': 'Internal',
        'Internal-Egress': 'Egress',
    }

    validate_move = str(
        move.location_id.location_type + '-' +
        move.location_dest_id.location_type)

    errors = []

    msg_validate = {
    }

    if validate_move not in __VALID_MOVES__:
        errors.append(
            '%s-%s Es un movimiento Inválido'
            % (move.location_id.name,
               move.location_dest_id.name))
    else:
        move.move_type = __MOVE_TYPE__[validate_move]

    if move.location_dest_id.name == move.location_id.name:
        errors.append(
            'La ubicación Destino no puede ser la misma '
            'que el Origen.')

    if move.package_id:
        if not move.package_id.location_id \
                and move.location_id.location_type != 'Ingress':
            errors.append(
                'El primer movimiento debe ser '
                'de tipo "Ingreso"')

        elif move.package_id.location_id != move.location_id \
                and move.location_id.location_type != 'Ingress':
            errors.append(
                'No puede mover desde %s '
                'porque no hay disponibilidad en la ubicación %s. '
                'Revise la disponibildad del paquete en las ubicaciones'
                % (move.location_id.name,
                   move.location_id.name))
        if move.package_id.pieces:
            if move.package_id.pieces != move.pieces:
                errors.append(
                    'Para mover paquetes, debe mover '
                    'la cantidad total disponible del paquete. '
                    'Actualmente el paquete tiene %s Piezas '
                    'y usted intenta mover %s piezas. Por favor corrija'
                    % (move.package_id.pieces, move.pieces))
    if move.unit_id:
        if not move.unit_id.location_id:
            if move.location_id.location_type != 'Ingress':
                errors.append('El primer movimiento debe ser de tipo ingreso')

        if move.unit_id.product_id.product_type == 'article' \
                and move.quantity != move.unit_id.product_id.article_qty:
            errors.append(
                'Este articulo debe moverse siempre '
                'con la cantidad fija de %s %s'
                % (move.unit_id.product_id.article_qty, measure))

        elif move.unit_id.fixed_ammount \
                and move.quantity != move.unit_id.quantity \
                and move.location_id.location_type != 'Ingress':
            errors.append(
                'Esta unidad debe moverse siempre '
                'con la cantidad fija de %s %s'
                % (move.unit_id.quantity, measure))
        elif move.quantity > move.unit_id.quantity \
                and move.location_id.location_type != 'Ingress':
            errors.append(
                'No hay %s %s disponible. '
                'La cantidad disponible de %s es de %s %s'
                % (move.quantity, measure,
                   item_move.code, move.unit_id.quantity, measure))
    return errors


def validate_stock_control(request, move):
    '''
    Diferentes validaciones previas a la creación del
    Control de Stock
    Si ocurre algún error en las validaciones,
    se agrega el mensaje de error a la lista 'errors'
    Finalmente la función devuelve la lista 'errors'
    '''
    errors = []
    '''
    stock_control_data diccionario que almacena
    datos del origen y destino del control de stock
    de la unidad. Si la unidad tiene un control de stock
    creado en la ubicacion origen del movimiento,
    esto se almacena en origin_data.
    Si tiene un control de stock creado
    en la ubicacion destino del movimiento,
    esto se almacena en dest_data
    '''

    stock_control_data = {
        'origin_data': False,
        'dest_data': False,
        }
    '''
    La lista unit_list se utiliza para almacenar
    Los ids de las unidades de producto, e iterar sobre ellos
    Tanto para movimientos de unidades indivuales: una sola iteración
    o paquetes: iteraciónes tantas unidades agrupe el paquete
    '''
    unit_list = []
    if move.unit_id:
        if move.unit_id.product_id.measure_id:
            measure = move.unit_id.product_id.measure_id.abbreviation
        else:
            measure = ' '
        unit_list.append(move.unit_id)

    if move.package_id:
        if move.package_id.product_id.measure_id:
            measure = move.package_id.product_id.measure_id.abbreviation
        else:
            measure = ' '
        unit_ids = ProductUnit.objects.filter(
            package_id=move.package_id, quantity__gte=0.000001)
        for unit_id in unit_ids:
            unit_list.append(unit_id)
    for unit_id in unit_list:
        if unit_id.stock_ctrl:
            if move.location_id.location_type != 'Ingress':
                # stck_ctrl_origin Es la ubicacion origen
                stck_ctrl_origin = StockControl.objects.filter(
                    unit_id=unit_id.id, location_id=move.location_id)
                if not stck_ctrl_origin:
                    errors.append(
                        'No puede mover la unidad desde la ubicación '
                        '%s porque la unidad no tiene Stock disponible '
                        'en esa ubicación. '
                        'Revise el Stock disponible y corrija. '
                        % (move.location_id))
                else:
                    for origin_data in stck_ctrl_origin:
                        stock_control_data['origin_data'] = origin_data
                        if origin_data.quantity < move.quantity \
                                and move.unit_id:
                            errors.append(
                                'No hay Stock disponible en %s. '
                                'Está tratando de mover %s %s pero la '
                                'cantidad disponible en %s es de %s %s. '
                                'Por favor Corrija '
                                % (move.location_id.name,
                                   move.quantity,
                                   measure,
                                   origin_data.location_id.name,
                                   origin_data.quantity,
                                   measure))
                        else:
                            stck_ctrl_dest = StockControl.objects.filter(
                                unit_id=unit_id.id,
                                location_id=move.location_dest_id)
                            if stck_ctrl_dest:
                                for dest_data in stck_ctrl_dest:
                                    stock_control_data['dest_data'] = dest_data
                            if not functions.create_stock_control(
                                    request, stock_control_data,
                                    unit_id, move):
                                errors.append(
                                    'Error creando el Control de Stock')
            else:
                errors.append('Esta unidad ya tuvo un ingreso')
        else:
            if not functions.create_stock_control(
                    request, stock_control_data, unit_id, move):
                errors.append('Error en la creación del Control de Stock')
    return errors
