-- select average number of retaken subjects per student
SPARQL

prefix ndbi040: <http://ndbi040/ontology/>

SELECT (AVG(?total_retakes) AS ?avg_retakes) WHERE {
  GRAPH <http://ndbi040/> {
    {
      SELECT (SUM(?retaken_subj_times - 1) AS ?total_retakes)
      WHERE {
        {
          SELECT ?student ?subj (COUNT(*) AS ?retaken_subj_times) WHERE {
            ?student a ndbi040:Student ;
              ndbi040:studies/ndbi040:instanceOf ?subj .
          }
          GROUP BY ?student ?subj
        }
      }
      GROUP BY ?student
    }
  }
}
