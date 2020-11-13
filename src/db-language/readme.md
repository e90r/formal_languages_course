# Mini script language for graph database queries #

## Syntax: ##

Script consists of 3 types of statements:

- `connect "%db_name%"` - set database directory
    - ### Example: 
        ```
        connect "/home/egor/db"
        ```

- `%production_head% : %production_body%` - add production to grammar
    - `%production_head%` is a string representation of production head
    - `%production_body%` can be a regular expression
    - ### Example: 
        ```
        S : term(a).nonterm(S).term(b).nonterm(S)
        S : e
        ```

- `select %obj% from %graph%` - get specified objective from graph
    - `%obj%` can be `count`, `edges` or `filter`
        - `count` will count a number of edges in graph
        - `edges` will return all edges (v, e, u) in graph
        - `filter (v, e, u) -> %BOOL_EXPR%` filters edges of a graph that match certain conditions
            - `%BOOL_EXPR%` could be a combination of:
                - `%edge% hasLbl %value%` checks if edge has specified label
                - `isStart %vertex%` checks if given vertex is in start set
                - `isFinal %vertex%` checks if given vertex is in final set

    - `%graph%` can represent graph with given name, grammar, regex or graph intersection
        - `"%graph_name%"` will load a graph file from database
        - `grammar` will take grammar that was defined with productions in the script
        - `[%pattern%]` will take regex of a given pattern 
        - `%graph_1% & %graph_2%` will take an intersection of graph1 and graph2
        - `setStartAndFinal %vertices% %vertices% %graph%` will take a graph with specified start and final vertices
            - `%vertices%` can be represented in following formats:
                - `{v1, v2, v3, ...}` - as a set
                - `n:m` - as a range from n to m
                - `_` - if you don't want to specify any certain vertices

    - ### Examples:
        ```
        select count edges from ("graph" & grammar)
        select count edges from (setStartAndFinal 0:6 {1,3,4} "graph")
        select filter (v, e, u) -> (e hasLbl abc) : edges from "graph"
        select filter (v, e, u) -> (e hasLbl abc & isStart v | !(isFinal u)) : edges from "graph"
        select edges from [term(a).term(b)*.(term(c)|term(d))+]
        ```
        