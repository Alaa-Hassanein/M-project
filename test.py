while True:
        x,y=graph.sample_evir()
        n=graph.number_of_nodes()
        graph.add_node(n,x,y)
        graph.add_edge(n-1,n)
        x1,y1=graph.x[n],graph.y[n]
        x2,y2=graph.x[n-1],graph.y[n-1]
        if (graph.isFree()):
            pygame.draw.circle(map.map,map.red,(graph.x[n],graph.y[n]),map.nodeRad,map.nodeThickness)
            if not graph.crossObstacle(x1,x2,y1,y2):
                pygame.draw.line(map.map,map.blue,(x1,y1),(x2,y2),map.edgeThickness)
