import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((640,480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        ## initialize opengl
        glClearColor(0.1,0.1,0.1,1)

        # AlphaBlned 모드
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

        self.shader = self.createShader("shaders/vertex.glsl", "shaders/fragment.glsl")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        self.cube = Cube(
            position=[0,0,-3],
            eulers = [0,0,0]
            )

        self.cubeMesh = CubeMesh()

        self.inputTexture = Material("textures/yiyaho.png")

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480,
            near = 0.1, far = 10, dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")
            
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

            ##update cube
            self.cube.eulers[2] += 0.2
            if(self.cube.eulers[2] > 360):
                self.cube.eulers[2] -=360

            ## refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)
            self.inputTexture.use()

            ## Base Matrix
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

            ## Rotation Matrix
            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )

            ## Translation Matrix
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2= pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )

            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)

            glBindVertexArray(self.cubeMesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cubeMesh.vertex_count)

            pg.display.flip()

            self.clock.tick(60)

        self.quit()

    def quit(self):
        
        self.cubeMesh.destroy()
        # self.triangle.destroy()
        self.inputTexture.destory()
        glDeleteProgram(self.shader)
        pg.quit()

class CubeMesh:

    def __init__(self):

        self.vertices = (
                    -0.5, -0.5, -0.5, 0, 0,
                    0.5, -0.5, -0.5, 1, 0,
                    0.5,  0.5, -0.5, 1, 1,

                    0.5,  0.5, -0.5, 1, 1,
                    -0.5,  0.5, -0.5, 0, 1,
                    -0.5, -0.5, -0.5, 0, 0,

                    -0.5, -0.5,  0.5, 0, 0,
                    0.5, -0.5,  0.5, 1, 0,
                    0.5,  0.5,  0.5, 1, 1,

                    0.5,  0.5,  0.5, 1, 1,
                    -0.5,  0.5,  0.5, 0, 1,
                    -0.5, -0.5,  0.5, 0, 0,

                    -0.5,  0.5,  0.5, 1, 0,
                    -0.5,  0.5, -0.5, 1, 1,
                    -0.5, -0.5, -0.5, 0, 1,

                    -0.5, -0.5, -0.5, 0, 1,
                    -0.5, -0.5,  0.5, 0, 0,
                    -0.5,  0.5,  0.5, 1, 0,

                    0.5,  0.5,  0.5, 1, 0,
                    0.5,  0.5, -0.5, 1, 1,
                    0.5, -0.5, -0.5, 0, 1,

                    0.5, -0.5, -0.5, 0, 1,
                    0.5, -0.5,  0.5, 0, 0,
                    0.5,  0.5,  0.5, 1, 0,

                    -0.5, -0.5, -0.5, 0, 1,
                    0.5, -0.5, -0.5, 1, 1,
                    0.5, -0.5,  0.5, 1, 0,

                    0.5, -0.5,  0.5, 1, 0,
                    -0.5, -0.5,  0.5, 0, 0,
                    -0.5, -0.5, -0.5, 0, 1,

                    -0.5,  0.5, -0.5, 0, 1,
                    0.5,  0.5, -0.5, 1, 1,
                    0.5,  0.5,  0.5, 1, 0,

                    0.5,  0.5,  0.5, 1, 0,
                    -0.5,  0.5,  0.5, 0, 0,
                    -0.5,  0.5, -0.5, 0, 1
                )

        self.vertex_count = len(self.vertices) // 5
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        ## Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

        ## UV
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class Triangle:
    def __init__(self):

        ## x, y ,z, r, g, b

        self.vertices = (
            # x     y    z    R    G    B    s    t    Nx   Ny   Nz  
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0,
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0
            )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 11

        ## Vertex Array Object를 만든다
        self.vao = glGenVertexArrays(1)
        ## 
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices,GL_STATIC_DRAW)

        ## [X,Y,Z r,g,b, s,t, Nx, Ny, Nz] 각 버텍스가 갖고있는 것
        # 
        # 그래픽 카드는 각 Buffer Array에 각 Index의 의미가 뭔지 모른다.
        # 각 인덱스의 Attribute를 Enable시켜줘야 인식할 수 있고,
        # 각 인덱스에서 몇번 Stride를 해야 Position인지, Coordinate인포메이션인지를 알 수 있따

        ## Position
        glEnableVertexAttribArray(0)
        ##24 stride 설명 : 32bit = 4byte, 버텍스마다 6개의 숫자 (3개Position, 3개 Color) 6*4byte = 24. 24개씩 Stride
        ## 0:Position, 3Attributes(Position)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(0))

        ## Vertex Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(12))
        
        ## Texture Coordinate
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(24))

        ## Normal Information
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(32))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

class Material:

    def __init__(self, filePath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        ## Convert는 일반 ALpha가 없을때 사용,
        ## Convert_Alpht는 Alpha이미지가 있으면
        image = pg.image.load(filePath).convert_alpha()
        image_width, image_height = image.get_rect().size

        ## OpenGL은 Pygame이 만들어낸 Image데이터를 읽지 못하기때문에, Image를 String으로 변환시켜서 넣어줘야한다
        image_data = pg.image.tostring(image, "RGBA")

        ## GL_UNSIGNED_BYTE = 0~255 range
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        ## Activate Texutre에는 Lightmap이나, Surface 등 여러 텍스쳐를 같이 불러올 수 있는데
        ## 이때 GL_TEXTURE0, GL_TEXTURE1등으로 여러개를 Activate시켜서 사용가능
        ## Activate Texture시에 Memory Allocation때문에 지워줘야함 destroy()
        glActiveTexture(GL_TEXTURE0) ## <-- Texture Location 0를 Active하겠다
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destory(self):
        glDeleteTextures(1, (self.texture, ))

if __name__ == "__main__":
    myApp = App()