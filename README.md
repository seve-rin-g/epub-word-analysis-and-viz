## Summary

Testing out a small app before moving onto replicating the large-dataset (high-frequency time-series) postgresdb that has comprised most of my past experience. 

Imports epubs, analyzes word frequency, updates the postgresDB with markers, and outputs visual analysis. 

*Screenshot goes here.*
## Functionality (Intentioned)

### Upload an epub file
- Perform word processing in Python
- Display a graph in d3 showing:
    - word frequency 
    - connections (adjacency)

### Filtering
- Enter a string like "bubbling" representing a word you are trying to find
- The viz will filter, showing words that match that description, or similar ones

## Development log

Although I've interacted with several (often very complex) postgres databases, I've never built one from scratch. 

I'm following this tutorial: https://www.youtube.com/watch?v=Pox10kU7d2c

022226: So far, most issues are syntax issues within the `init.sql` and addressed via finding errors in `docker compose logs postgres`.      
022326: Another thing to watch out for: docker caching previous `Dockerfile`s -- address with `docker-compose build --no-cache`.
022426: Flask app working, postgres/pgadmin/web are all working in dev. Time to work on epub importing and visualization (the fun stuff).
022626: NLP library integration
