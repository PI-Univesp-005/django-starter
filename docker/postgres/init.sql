

-- -- docker/postgres/init.sql
-- --
-- -- This script runs exactly once: when the PostgreSQL container starts against
-- -- an empty data volume. If the volume already has data (i.e. on every restart
-- -- after the first), PostgreSQL skips this file entirely.
-- --
-- -- What belongs here:
-- --   - Extensions that must exist before any connection or migration runs
-- --   - Database-level encoding / locale verification
-- --   - Grants or roles your application user needs beyond the defaults
-- --
-- -- What does NOT belong here:
-- --   - Creating tables that Django models represent — use migrations for that.
-- --     If you create a table here, Django's migration system doesn't know it
-- --     exists, which breaks `migrate --run-syncdb`, schema introspection and
-- --     the entire migration dependency graph.

-- -- Confirm the database is set to UTF-8. The official postgres:17 image
-- -- already defaults to UTF8, but making it explicit serves as documentation.
-- -- This will raise a notice (not an error) if it's already set correctly.
-- DO $$
-- BEGIN
--   IF current_setting('server_encoding') <> 'UTF8' THEN
--     RAISE EXCEPTION 'Database encoding must be UTF8, got: %', current_setting('server_encoding');
--   END IF;
-- END $$;

-- -- Enable the pg_trgm extension (trigram similarity search).
-- -- Useful for LIKE/ILIKE acceleration and fuzzy search on text fields.
-- -- Creating it here ensures it is available to any migration that might use it.
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- -- Enable the unaccent extension (accent-insensitive text search).
-- -- Common need for Portuguese and other accented-language applications.
-- CREATE EXTENSION IF NOT EXISTS unaccent;

-- -- Confirm setup completed. This message appears in the container log on
-- -- first start, making it easy to verify the script ran.
-- DO $$ BEGIN
--   RAISE NOTICE 'init.sql completed — extensions enabled: pg_trgm, unaccent';
-- END $$;

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
