                                                                
       moonNode = sg.SceneGraphNode('moonNode')   
       moonNode.transform = [[0.02 0.   0.   0.  ]
 [0.   0.02 0.   0.  ]
 [0.   0.   0.02 0.  ]
 [0.   0.   0.   1.  ]]                
       moonNode.childs += [None]
      
                                                                
       moonRotation = sg.SceneGraphNode('moonRotation')   
       moonRotation.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       moonRotation.childs += [moonNode]
      
                                                                
       moonPosition = sg.SceneGraphNode('moonPosition')   
       moonPosition.transform = [[1.  0.  0.  0.3]
 [0.  1.  0.  0. ]
 [0.  0.  1.  0. ]
 [0.  0.  0.  1. ]]                
       moonPosition.childs += [moonRotation]
      
                                                                
       moonSystem = sg.SceneGraphNode('moonSystem')   
       moonSystem.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       moonSystem.childs += [moonPosition]
      
                                                                
       earthNode = sg.SceneGraphNode('earthNode')   
       earthNode.transform = [[0.1 0.  0.  0. ]
 [0.  0.1 0.  0. ]
 [0.  0.  0.1 0. ]
 [0.  0.  0.  1. ]]                
       earthNode.childs += [None]
      
                                                                
       earthRotation = sg.SceneGraphNode('earthRotation')   
       earthRotation.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       earthRotation.childs += [earthNode]
      
                                                                
       earthPosition = sg.SceneGraphNode('earthPosition')   
       earthPosition.transform = [[1.  0.  0.  1.5]
 [0.  1.  0.  0. ]
 [0.  0.  1.  0. ]
 [0.  0.  0.  1. ]]                
       earthPosition.childs += [earthRotation, moonSystem]
      
                                                                
       earthSystem = sg.SceneGraphNode('earthSystem')   
       earthSystem.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       earthSystem.childs += [earthPosition]
      
                                                                
       sunNode = sg.SceneGraphNode('sunNode')   
       sunNode.transform = [[0.3 0.  0.  0. ]
 [0.  0.3 0.  0. ]
 [0.  0.  0.3 0. ]
 [0.  0.  0.  1. ]]                
       sunNode.childs += [None]
      
                                                                
       sunRotation = sg.SceneGraphNode('sunRotation')   
       sunRotation.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       sunRotation.childs += [sunNode]
      
                                                                
       solarSystem = sg.SceneGraphNode('solarSystem')   
       solarSystem.transform = [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]                
       solarSystem.childs += [sunRotation, earthSystem]
      
