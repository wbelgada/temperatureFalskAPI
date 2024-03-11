CREATE TABLE locations (
	lon float,
	lat float,
	slug text,
	-- Create an index on the 'slug' column
    CONSTRAINT location_slug_idx UNIQUE (slug)
);