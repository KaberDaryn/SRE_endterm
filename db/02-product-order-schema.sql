-- ─── PRODUCT SERVICE DB ───
\connect product;

CREATE TABLE IF NOT EXISTS product (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) UNIQUE NOT NULL,
    price       NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    image       VARCHAR(500),
    date_created TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_slug ON product(slug);

INSERT INTO product (name, slug, price, image) VALUES
    ('Laptop',  'laptop',  1200.00, 'product1.jpg'),
    ('Phone',   'phone',   800.00,  'product2.jpg'),
    ('Camera',  'camera',  500.00,  'sample.jpg')
ON CONFLICT DO NOTHING;

-- ─── ORDER SERVICE DB ───
\connect orders;

CREATE TABLE IF NOT EXISTS "order" (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL,
    is_open      BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_item (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER REFERENCES "order"(id) ON DELETE CASCADE,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_order_user ON "order"(user_id);
CREATE INDEX IF NOT EXISTS idx_order_open ON "order"(is_open);
