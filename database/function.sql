CREATE OR REPLACE FUNCTION insert_or_update_location_temp(
    p_slug TEXT,
    p_minTemp TEXT,
    p_maxTemp TEXT
)
RETURNS VOID AS $$
BEGIN
    -- Check if there is an existing record with the same day, lineid, and tripid
    PERFORM 1
    FROM temp2mstore
    WHERE slug = p_slug;

    IF FOUND THEN
        -- Update the existing record
        UPDATE temp2mstore
        SET
			max_temperature = appendsequence(temp2mstore.max_temperature,p_maxTemp::tfloat),
            min_temperature = appendsequence(temp2mstore.min_temperature,p_minTemp::tfloat)
        WHERE
            slug = p_slug;
    ELSE
        -- Insert a new record
        INSERT INTO temp2mstore (slug, min_temperature, max_temperature)
        VALUES (p_slug, p_minTemp::tfloat, p_maxTemp::tfloat);
    END IF;
END;
$$ LANGUAGE plpgsql;