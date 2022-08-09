import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader



class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((500,400),pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        ## initialize opengl
        glClearColor(0.1,0.1,0.1,1)
        self.shader = self.createShader("shaders/vertex.glsl", "shaders/fragment.glsl")
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    def createShader(self, vertexFilePath, fragmentFilePath):
        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True

        while(running):
            for event in pg.event.get():
                if( event.type==pg.QUIT):
                    running=False

            ## refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            self.clock.tick(60)

        self.quit()

    def quit(self):
        pg.quit()


class Triangle:
    def __init__(self):

        ## x, y ,z, r, g, b

        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
            )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices,GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        ##24 stride 설명 : 32bit = 4byte, 버텍스마다 6개의 숫자 (3개Position, 3개 Color) 6*4byte = 24. 24개씩 Stride
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))


    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))



if __name__ == "__main__":
    myApp = App()