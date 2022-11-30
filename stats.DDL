CREATE TABLE IF NOT EXISTS public.stats (
	id uuid NOT NULL,
	"date" date NULL,
	"views" int4 NULL,
	clicks int4 NULL,
	"cost" numeric(5, 2) NULL,
	CONSTRAINT stats_pkey PRIMARY KEY (id)
);
