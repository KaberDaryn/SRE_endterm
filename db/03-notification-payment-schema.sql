-- ─── NOTIFICATION SERVICE DB ───
\connect notifications;

CREATE TABLE IF NOT EXISTS notification (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL,
    message           VARCHAR(500) NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'email',
    status            VARCHAR(20) DEFAULT 'pending',
    date_created      TIMESTAMP DEFAULT NOW(),
    date_sent         TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notif_user ON notification(user_id);
CREATE INDEX IF NOT EXISTS idx_notif_status ON notification(status);

-- ─── PAYMENT SERVICE DB ───
\connect payments;

CREATE TABLE IF NOT EXISTS payment (
    id              SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    amount          NUMERIC(10, 2) NOT NULL,
    currency        VARCHAR(10) DEFAULT 'USD',
    status          VARCHAR(20) DEFAULT 'pending',
    payment_method  VARCHAR(50) DEFAULT 'card',
    transaction_id  VARCHAR(255) UNIQUE,
    date_created    TIMESTAMP DEFAULT NOW(),
    date_updated    TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payment_order ON payment(order_id);
CREATE INDEX IF NOT EXISTS idx_payment_user ON payment(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_status ON payment(status);
