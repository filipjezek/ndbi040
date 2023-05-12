-- select teachers who teach subject A and students who studied subject A but had
-- a different teacher

-- this cannot be done using sparql operator FILTER NOT EXISTS,
-- because the underlying data are relational tables
-- and virtuoso complains about too many variables in state:
-- SQ156: Internal Optimized compiler error : Query too large, variables in state over the limit in sqlvec.c:3026.

SELECT * FROM (
  SPARQL
  PREFIX ndbi040: <http://ndbi040/ontology/>
  PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>

  SELECT ?teacher ?student ?subj WHERE {
    GRAPH <http://ndbi040/> {
      ?teacher a ndbi040:Teacher ;
        aiiso:teaches/ndbi040:instanceOf ?subj .
      ?student a ndbi040:Student ;
        ndbi040:studies/ndbi040:instanceOf ?subj .
    }
  }
) AS X
EXCEPT
SELECT * FROM (
  SPARQL

  PREFIX ndbi040: <http://ndbi040/ontology/>
  PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>

  SELECT ?teacher ?student ?subj WHERE {
    GRAPH <http://ndbi040/> {
      ?teacher a ndbi040:Teacher ;
        aiiso:teaches ?subj_inst .
      ?student a ndbi040:Student ;
        ndbi040:studies ?subj_inst .
      ?subj_inst ndbi040:instanceOf ?subj .
    }
  }
) AS Y
