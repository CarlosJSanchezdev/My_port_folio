-- Reparar secuencia de contact_messages
SELECT setval('contact_messages_id_seq', COALESCE((SELECT MAX(id) FROM contact_messages), 1));

-- Eliminar columnas que no existen en el modelo actual
ALTER TABLE contact_messages DROP COLUMN IF EXISTS user_id;
ALTER TABLE contact_messages DROP COLUMN IF EXISTS verification_level;
ALTER TABLE contact_messages DROP COLUMN IF EXISTS verified_email;
