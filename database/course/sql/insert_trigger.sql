CREATE OR REPLACE FUNCTION course_before_insert_update_trigger()
RETURNS trigger AS $$
BEGIN
  IF NEW.instructor_id IS NULL THEN
    RAISE EXCEPTION 'Instructor ID cannot be null';
  END IF;

  SELECT 1
  FROM instructor
  WHERE id = NEW.instructor_id
  AND is_instructor = TRUE;

  IF FOUND THEN
    RETURN NEW;
  ELSE
    RAISE EXCEPTION 'Instructor does not exist or is not an instructor.';
  END IF;
END;
$$ LANGUAGE plpgsql;
