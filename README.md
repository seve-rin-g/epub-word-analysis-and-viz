## Summary

I wanted to address some gaps in my understanding of backend, so I'm building this small app before moving onto replicating a larger time-series postgresdb. 

*One-liner about this app.*

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

### Common issues
- syntax issues within the `init.sql`, addressed via finding errors in `docker compose logs postgres`
- docker caching previous `Dockerfile`s -- address with `docker-compose build --no-cache`