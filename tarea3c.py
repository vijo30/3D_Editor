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
import json
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import random
import imgui
from imgui.integrations.glfw import GlfwRenderer
import os.path
import grafica.performance_monitor as pm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls
import grafica.transformations as tr
from examples.ex_scene_graph_solar import createSystem

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

    edited, locationX = imgui.slider_float("Location X", locationX, -10.0, 10.0)
    edited, locationY = imgui.slider_float("Location Y", locationY, -10.0, 10.0)
    edited, locationZ = imgui.slider_float("Location Z", locationZ, -10.0, 10.0)
    edited, angleXY = imgui.slider_float("Angle XY", angleXY, -np.pi, np.pi)
    edited, angleYZ = imgui.slider_float("Angle YZ", angleYZ, -np.pi, np.pi)
    edited, angleXZ = imgui.slider_float("Angle XZ", angleXZ, -np.pi, np.pi)
    edited, scaleX = imgui.slider_float("Scale X", scaleX, 0.0, 4.0)
    edited, scaleY = imgui.slider_float("Scale Y", scaleY, 0.0, 4.0)
    edited, scaleZ = imgui.slider_float("Scale Z", scaleZ, 0.0, 4.0)
    show, _ = imgui.collapsing_header("Nodes") 
    global controller
    
    transform = tr.matmul(
                [tr.translate(locationX, locationY, locationZ),
                tr.rotationZ(angleXY),
                tr.rotationY(angleXZ),
                tr.rotationX(angleYZ),
                tr.scale(scaleX, scaleY, scaleZ)]
                )

    scene.transform = tr.matmul([const, transform])
    if show:
      if imgui.tree_node(text=str(scene.name)):
        iterateNode(scene)
    
    if imgui.button(label="Save"):
      scene_save = [scene.to_string()]
      scene_saved = generateTree(scene_save, scene)
      with open("save.txt", "w") as fp:
        fp.seek(0)
        for item in scene_saved:
           fp.write("%s\n" % item)
        fp.truncate()
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
    edited, locationX = imgui.slider_float("Location X", locationX, -10.0, 10.0)
    edited, locationY = imgui.slider_float("Location Y", locationY, -10.0, 10.0)
    edited, locationZ = imgui.slider_float("Location Z", locationZ, -10.0, 10.0)
    edited, angleXY = imgui.slider_float("Angle XY", angleXY, -np.pi, np.pi)
    edited, angleYZ = imgui.slider_float("Angle YZ", angleYZ, -np.pi, np.pi)
    edited, angleXZ = imgui.slider_float("Angle XZ", angleXZ, -np.pi, np.pi)
    edited, scaleX = imgui.slider_float("Scale X", scaleX, 0.0, 4.0)
    edited, scaleY = imgui.slider_float("Scale Y", scaleY, 0.0, 4.0)
    edited, scaleZ = imgui.slider_float("Scale Z", scaleZ, 0.0, 4.0)
    
    return locationX, locationY, locationZ, angleXY, angleYZ, angleXZ, scaleX, scaleY, scaleZ

def iterateNode(scene):

    for i in range(0,len(scene.childs)):

      if imgui.tree_node(text=str(scene.childs[i].name)):
        imgui.same_line()
        imgui.text("(selected)")
        if not isinstance(scene.childs[i].childs[0],GPUShape):
          iterateNodeRecursive(scene.childs[i])

        imgui.begin("Configuration sliders: "+ str(scene.childs[i].name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        


        scene.childs[i].parameters = \
  transformGuiOverlayNode(scene.childs[i].parameters[0], scene.childs[i].parameters[1], scene.childs[i].parameters[2], scene.childs[i].parameters[3], scene.childs[i].parameters[4], 
                          scene.childs[i].parameters[5], scene.childs[i].parameters[6], scene.childs[i].parameters[7], scene.childs[i].parameters[8])

        scene.childs[i].transform = tr.matmul([
              tr.translate(scene.childs[i].parameters[0], scene.childs[i].parameters[1], scene.childs[i].parameters[2]),
              tr.rotationZ(scene.childs[i].parameters[3]),
              tr.rotationY(scene.childs[i].parameters[4]),
              tr.rotationX(scene.childs[i].parameters[5]),
              tr.scale(scene.childs[i].parameters[6], scene.childs[i].parameters[7], scene.childs[i].parameters[8])])
        


        
        imgui.end()

        imgui.tree_pop()
        


    imgui.tree_pop()

def iterateNodeRecursive(scene):
  for i in range(0,len(scene.childs)):
    if imgui.tree_node(text=str(scene.childs[i].name)):
      imgui.same_line()
      imgui.text("(selected)")
      if not isinstance(scene.childs[i].childs[0],GPUShape):
          iterateNodeRecursive(scene.childs[i])
      imgui.begin("Configuration sliders: "+ str(scene.childs[i].name), False, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
      
      
        
      scene.childs[i].parameters = \
transformGuiOverlayNode(scene.childs[i].parameters[0], scene.childs[i].parameters[1], scene.childs[i].parameters[2], scene.childs[i].parameters[3], scene.childs[i].parameters[4], 
                        scene.childs[i].parameters[5], scene.childs[i].parameters[6], scene.childs[i].parameters[7], scene.childs[i].parameters[8])

      scene.childs[i].transform = tr.matmul([ 
            tr.translate(scene.childs[i].parameters[0], scene.childs[i].parameters[1], scene.childs[i].parameters[2]),
            tr.rotationZ(scene.childs[i].parameters[3]),
            tr.rotationY(scene.childs[i].parameters[4]),
            tr.rotationX(scene.childs[i].parameters[5]),
            tr.scale(scene.childs[i].parameters[6], scene.childs[i].parameters[7], scene.childs[i].parameters[8])])
      


      
      imgui.end()

      imgui.tree_pop()
        
        

    


    




# Initialize glfw
if not glfw.init():
    glfw.set_window_should_close(window, True)

width = 1280
height = 720
title = "Interactive Transform Generator"
window = glfw.create_window(width, height, title, None, None)

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












t0 = glfw.get_time()
camera_theta = np.pi / 4
cameraZ = 2
perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
scene = createSystem(lightingPipeline)



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
const = scene.transform 

def generateTree(a, scene):
  for i in range(0,len(scene.childs)):
      a.append(scene.childs[i].to_string())
      if not isinstance(scene.childs[i].childs[0],GPUShape):
          generateTree(a, scene.childs[i]) 

  
  return a[::-1]

print(scene.childs[0].to_string())
print(sg.findNode(scene, 'sunNode').transform)

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
            # Measuring performance
    perfMonitor.update(glfw.get_time())
    glfw.set_window_title(window, title + str(perfMonitor))

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
