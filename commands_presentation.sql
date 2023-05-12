SPARQL
PREFIX ndbi040: <http://ndbi040/ontology/>

INSERT DATA {
  GRAPH <http://ndbi040/> {
    <http://ndbi040/data/person/10000> a foaf:Person ;
      a ndbi040:Student​ ;
      foaf:name "Anakin Skywalker" .
  }
};

SPARQL
PREFIX ndbi040: <http://ndbi040/ontology/>

WITH <http://ndbi040/>
INSERT { ?student ndbi040:studies ?sample }
WHERE
{
  ?student foaf:name "Anakin Skywalker" .
  {
    SELECT (SAMPLE(?subj_inst) AS ?sample)
    WHERE {
      ?subj_inst a ndbi040:SubjectInstance
    }
  }
};

SPARQL
PREFIX ndbi040: <http://ndbi040/ontology/>
PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#>

SELECT ?name
WHERE {
  GRAPH <http://ndbi040/> {
    ?person foaf:name "Anakin Skywalker" ;
      ndbi040:studies/^aiiso:teaches/foaf:name ?name .
  }
};

SPARQL
PREFIX ndbi040: <http://ndbi040/ontology/>

WITH <http://ndbi040/>
DELETE { ?person ?pred ?obj }
WHERE {
  ?person foaf:name "Anakin Skywalker" ;
    ?pred ?obj .
};

SPARQL
PREFIX ndbi040: <http://ndbi040/ontology/>

ASK {
  GRAPH <http://ndbi040/> {
    ?person foaf:name "Anakin Skywalker" .
  }
};