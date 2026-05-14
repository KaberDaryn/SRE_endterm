-- ============================================================
-- SRE End-Term Project — Database Schemas
-- Student: Kaber Daryn | SE-2430
-- ============================================================

-- ─── USER SERVICE DB ───
\connect user;

CREATE TABLE IF NOT EXISTS "user" (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    api_key     VARCHAR(255) UNIQUE,
    date_created TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_user_api_key ON "user"(api_key);

INSERT INTO "user" (name, email, password, api_key)
VALUES ('Admin', 'admin@sre.local', 'hashed_password', 'admin-api-key-001')
ON CONFLICT DO NOTHING;
