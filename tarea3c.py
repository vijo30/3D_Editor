# coding=utf-8
"""
Simple example using ImGui with GLFW and OpenGL.

More info at:
https://pypi.org/project/imgui/

Installation:
pip install imgui[glfw]

Another example:
https://github.com/swistakm/pyimgui/blob/master/doc/examples/integrations_glfw3.py#L2
"""
import glfw
import pickle
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import random
import imgui
from imgui.integrations.glfw import GlfwRenderer
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import grafica.transformations as tr

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)



def transformGuiOverlay(locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ, scene):
    # start new frame context
    imgui.new_frame()

    # open new window context
    imgui.begin("3D Transformations control", False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)

    # draw text label inside of current window
    imgui.text("Configuration sliders: "+ str(scene.name))

    edited, locationX = imgui.slider_float("location X", locationX, -1.0, 1.0)
    edited, locationY = imgui.slider_float("location Y", locationY, -1.0, 1.0)
    edited, locationZ = imgui.slider_float("location Z", locationZ, -1.0, 1.0)
    edited, angleXY = imgui.slider_float("AngleXY", angleXY, -np.pi, np.pi)
    edited, angleYZ = imgui.slider_float("AngleYZ", angleYZ, -np.pi, np.pi)
    edited, angleXZ = imgui.slider_float("AngleXZ", angleXZ, -np.pi, np.pi)
    edited, scaleX = imgui.slider_float("scale X", scaleX, 0.0, 3.0)
    edited, scaleY = imgui.slider_float("scale Y", scaleY, 0.0, 3.0)
    edited, scaleZ = imgui.slider_float("scale Z", scaleZ, 0.0, 3.0)
    show, _ = imgui.collapsing_header("Nodes") 
    global controller
    
    transform = tr.matmul(
                [tr.translate(locationX, locationY, locationZ),
                tr.rotationZ(angleXY),
                tr.rotationY(angleXZ),
                tr.rotationX(angleYZ),
                tr.scale(scaleX, scaleY, scaleZ)]
                )
    
    scene.transform = tr.matmul([scene.transform, transform])
    if show:
      if imgui.tree_node(text=str(scene.name)):
        iterateNode(scene)
    
    if imgui.button(label="Save"):
      with open("copia1.py", "wb") as sc:
        pickle.dump(scene, sc, pickle.HIGHEST_PROTOCOL)
      print("Saved")



          



    edited, checked = imgui.checkbox("wireframe", not controller.fillPolygon)
      
    
    if edited:
        controller.fillPolygon = not checked

    # close current window context
    imgui.end()

    # pass all drawing comands to the rendering pipeline
    # and close frame context
    imgui.render()
    imgui.end_frame()

    return locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ, scene

def transformGuiOverlayNode(locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ):
    edited, locationX = imgui.slider_float("location X", locationX, -1.0, 1.0)
    edited, locationY = imgui.slider_float("location Y", locationY, -1.0, 1.0)
    edited, locationZ = imgui.slider_float("location Z", locationZ, -1.0, 1.0)
    edited, angleXY = imgui.slider_float("AngleXY", angleXY, -np.pi, np.pi)
    edited, angleYZ = imgui.slider_float("AngleYZ", angleYZ, -np.pi, np.pi)
    edited, angleXZ = imgui.slider_float("AngleXZ", angleXZ, -np.pi, np.pi)
    edited, scaleX = imgui.slider_float("scale X", scaleX, 0.0, 3.0)
    edited, scaleY = imgui.slider_float("scale Y", scaleY, 0.0, 3.0)
    edited, scaleZ = imgui.slider_float("scale Z", scaleZ, 0.0, 3.0)
    
    return locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ

def iterateNode(scene):

    for i in range(0,len(scene.childs)):

        if imgui.tree_node(text=str(scene.childs[i].name)):
            imgui.same_line()
            imgui.text("(selected)")
            if not isinstance(scene.childs[i].childs[0],GPUShape):
              iterateNodeRecursive(scene.childs[i])

            imgui.begin(str(scene.childs[i].name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            


            variableList[i] = \
      transformGuiOverlayNode(variableList[i][0], variableList[i][1], variableList[i][2], variableList[i][3], variableList[i][4], 
                              variableList[i][5], variableList[i][6], variableList[i][7], variableList[i][8])

            scene.childs[i].transform = tr.matmul([scene.childs[i].transform, 
                  tr.translate(variableList[i][0], variableList[i][1], variableList[i][2]),
                  tr.rotationZ(variableList[i][3]),
                  tr.rotationY(variableList[i][4]),
                  tr.rotationX(variableList[i][5]),
                  tr.scale(variableList[i][6], variableList[i][7], variableList[i][8])])
            


            
            imgui.end()

            imgui.tree_pop()
        


    imgui.tree_pop()

def iterateNodeRecursive(scene):
  for i in range(0,len(scene.childs)):
        if imgui.tree_node(text=str(scene.childs[i].name)):
            imgui.same_line()
            imgui.text("(selected)")
            imgui.begin(str(scene.childs[i].name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            
            
              
            variableList[i] = \
      transformGuiOverlayNode(variableList[i][0], variableList[i][1], variableList[i][2], variableList[i][3], variableList[i][4], 
                              variableList[i][5], variableList[i][6], variableList[i][7], variableList[i][8])

            scene.childs[i].transform = tr.matmul([scene.childs[i].transform, 
                  tr.translate(variableList[i][0], variableList[i][1], variableList[i][2]),
                  tr.rotationZ(variableList[i][3]),
                  tr.rotationY(variableList[i][4]),
                  tr.rotationX(variableList[i][5]),
                  tr.scale(variableList[i][6], variableList[i][7], variableList[i][8])])
            


            
            imgui.end()

            imgui.tree_pop()
        





    

      

def create_tree(pipeline):
    # Piramide verde
    green_pyramid =  bs.createColorNormalsCube(0, 1, 0)
    gpuGreenPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreenPyramid)
    gpuGreenPyramid.fillBuffers(green_pyramid.vertices, green_pyramid.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_quad = bs.createColorNormalsCube(139/255, 69/255, 19/255)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brown_quad.vertices, brown_quad.indices, GL_STATIC_DRAW)

    # Tronco
    tronco = sg.SceneGraphNode("Tronco")
    tronco.transform = tr.scale(0.05, 0.05, 0.2)
    tronco.childs += [gpuBrownQuad]

    # Hojas
    hojas = sg.SceneGraphNode("Hojas")
    hojas.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.uniformScale(0.25)])
    hojas.childs += [gpuGreenPyramid]

    # Arbol
    tree = sg.SceneGraphNode("Arbol")
    tree.transform = tr.identity()
    tree.childs += [tronco, hojas]

    return tree



def createCar(pipeline, r, g, b):
    # Creating shapes on GPU memory
    blackCube = bs.createColorNormalsCube(0, 0, 0)
    gpuBlackCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlackCube)
    gpuBlackCube.fillBuffers(blackCube.vertices, blackCube.indices, GL_STATIC_DRAW)

    chasisCube = bs.createColorNormalsCube(r, g, b)
    gpuChasisCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuChasisCube)
    gpuChasisCube.fillBuffers(chasisCube.vertices, chasisCube.indices, GL_STATIC_DRAW)

    # Cheating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr.scale(0.2, 0.8, 0.2)
    wheel.childs += [gpuBlackCube]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr.translate(0.3, 0, -0.3)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr.translate(-0.3, 0, -0.3)
    backWheel.childs += [wheelRotation]

    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(1, 0.7, 0.5)
    chasis.childs += [gpuChasisCube]

    # All pieces together
    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    return car



# Initialize glfw
if not glfw.init():
    glfw.set_window_should_close(window, True)

width = 1280
height = 720

window = glfw.create_window(width, height, "GLFW OpenGL ImGui", None, None)

if not window:
    glfw.terminate()
    glfw.set_window_should_close(window, True)
    
# Resize window
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

glfw.make_context_current(window)


def createGPUShape(pipeline, shape):
  gpuShape = es.GPUShape().initBuffers()
  pipeline.setupVAO(gpuShape)
  gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
  return gpuShape

# Creating our shader program and telling OpenGL to use it
lightingPipeline = ls.SimplePhongShaderProgram()
glUseProgram(lightingPipeline.shaderProgram)

# Setting up the clear screen color
glClearColor(0.8, 0.8, 0.8, 1.0)

glEnable(GL_DEPTH_TEST)
projection = tr.perspective(45, float(width) / float(height), 0.1, 100)
# Creating shapes on GPU memory


# initilize imgui context (see documentation)
imgui.create_context()
impl = GlfwRenderer(window)

# Connecting the callback function 'on_key' to handle keyboard events
# It is important to set the callback after the imgui setup
glfw.set_key_callback(window, on_key)
glfw.set_window_size_callback(window, window_resize)




locationX = 0.0
locationY = 0.0
locationZ = 0.0
angleXY = 0.0
angleYZ = 0.0
angleXZ = 0.0
scaleX = 1.0
scaleY = 1.0
scaleZ = 1.0


tuple = (0, 0, 0, 0, 0, 0, 1, 1, 1)

#scene = create_tree(lightingPipeline)
scene = createCar(lightingPipeline, 1, 0, 0)
print(scene.name)
print(scene.childs[0].name)
print(scene.childs[0].transform)
variableList = []

def addVariables(scene):
  i = 0
  while i < len(scene.childs):
    if not isinstance(scene.childs[i].childs[0],GPUShape):
      addVariables(scene.childs[i])
    variableList.append(tuple)
    i += 1

addVariables(scene)

print(variableList)



t0 = glfw.get_time()
camera_theta = np.pi / 4
cameraZ = 0

while not glfw.window_should_close(window):

    impl.process_inputs()
    # Using GLFW to check for input events

    # Poll and handle events (inputs, window resize, etc.)
    # You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
    # - When io.want_capture_mouse is true, do not dispatch mouse input data to your main application.
    # - When io.want_capture_keyboard is true, do not dispatch keyboard input data to your main application.
    # Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
    # io = imgui.get_io()
    # print(io.want_capture_mouse, io.want_capture_keyboard)
    glfw.poll_events()
    
    t1 = glfw.get_time()
    dt = t1 - t0
    t0 = t1
    # Clearing the screen in both, color and depth
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    # Filling or not the shapes depending on the controller state
    if (controller.fillPolygon):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)



    # imgui function
    impl.process_inputs()
    if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
        camera_theta -= 2 * dt

    if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
        camera_theta += 2 * dt
        
    if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
        cameraZ += 2 * dt
        
    if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
        cameraZ -= 2 * dt    
    camX = 3 * np.sin(camera_theta)
    camY = 3 * np.cos(camera_theta)
    camZ = cameraZ
    viewPos = np.array([camX, camY, camZ])
    view = tr.lookAt(
      viewPos,
      np.array([0, 0, 0]),
      np.array([0, 0, 1])
      )
    
    scene = createCar(lightingPipeline, 1, 0, 0)
    
    locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ, scene = \
        transformGuiOverlay(locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ, scene)

    # Setting uniforms and drawing the Quad


    
    
    
    # Setting all uniform shader variables

    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    # TO DO: Explore different parameter combinations to understand their effect!

    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 4, 4, 4)
    glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1],
                viewPos[2])
    glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)

    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
    glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    
    
    sg.drawSceneGraphNode(scene, lightingPipeline, "model")
    # Drawing the imgui texture over our drawing
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    impl.render(imgui.get_draw_data())

    # Once the render is done, buffers are swapped, showing only the complete scene.
    glfw.swap_buffers(window)

# freeing GPU memory
scene.clear()

impl.shutdown()
glfw.terminate()
