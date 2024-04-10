
insert into
    main.users (
        user_id,
        first_name,
        last_name,
        is_admin,
        created_at,
        register_status
    )
values
    (1, 'dash', 'cool', 0, CURRENT_TIMESTAMP, 1),
    (2, 'admin', 'root', 1, CURRENT_TIMESTAMP, 1);

INSERT INTO
    locations (
        longitude,
        latitude,
        user_id,
        created_at,
        register_status
    )
VALUES
    (-74.0059413, 40.7127837, 1, CURRENT_TIMESTAMP, 1),
    (-0.127758, 51.507351, 1, CURRENT_TIMESTAMP, 1),
    (2.3522219, 48.856614, 1, CURRENT_TIMESTAMP, 1),
    (13.405, 52.52, 1, CURRENT_TIMESTAMP, 1),
    (151.209296, -33.86882, 1, CURRENT_TIMESTAMP, 1),
    (-46.633309, -23.55052, 1, CURRENT_TIMESTAMP, 1),
    (-99.133208, 19.4326077, 1, CURRENT_TIMESTAMP, 1),
    (139.6917064, 35.6894875, 1, CURRENT_TIMESTAMP, 1),
    (37.6173, 55.755826, 1, CURRENT_TIMESTAMP, 1),
    (-3.7037902, 40.4167754, 1, CURRENT_TIMESTAMP, 1);


INSERT INTO
    categories (name, user_id, created_at, register_status)
VALUES
    ('Restaurante', 1, CURRENT_TIMESTAMP, 1),
    ('Parque', 1, CURRENT_TIMESTAMP, 1),
    ('Museo', 1, CURRENT_TIMESTAMP, 1),
    ('Biblioteca', 1, CURRENT_TIMESTAMP, 1),
    ('Centro Comercial', 1, CURRENT_TIMESTAMP, 1);