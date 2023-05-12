-- select address (which is stored in a graph) into a relational table

SELECT p.*, a.city, a.street, a.postcode FROM people AS p JOIN (
SPARQL

PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>

SELECT ?person ?street ?city ?postcode WHERE {
  GRAPH <http://ndbi040/> {
    ?person a foaf:Person;
      vcard:hasAddress ?addr .
    ?addr vcard:locality ?city ;
      vcard:street-address ?street ;
      vcard:postal-code ?postcode .
  }
}) AS a
ON p.id = sprintf_inverse(a.person, 'http://ndbi040/data/person/%d', 2)[0]

