import basilisk as bsk
import pygame as pg
import numpy as np
import moderngl as mgl


class RenderHandler:
    def __init__(self, game) -> None:
        self.game = game
        self.engine = game.engine


        self.default_shader = self.engine.shader
        # Shaders
        self.sight_shader  = bsk.Shader(self.engine, vert='shaders/sight_prepass.vert', frag='shaders/sight_prepass.frag')
        self.dim_shader    = bsk.Shader(self.engine, vert='shaders/dim.vert',           frag='shaders/dim.frag')
        self.geo_shader    = bsk.Shader(self.engine, vert='shaders/geometry.vert',      frag='shaders/geometry.frag')
        self.norm_shader   = bsk.Shader(self.engine, vert='shaders/normal.vert',        frag='shaders/normal.frag')
        self.output_shader = bsk.Shader(self.engine, vert='shaders/output.vert',        frag='shaders/output.frag')
        self.outline_combine_shader = bsk.Shader(self.engine, vert='shaders/combine_outlines.vert', frag='shaders/combine_outlines.frag')

        # First render pass
        self.sight_prepass = bsk.Framebuffer(self.engine)
        self.edge_sight    = bsk.Framebuffer(self.engine)
        self.edge_normal   = bsk.Framebuffer(self.engine)
        self.geometry      = bsk.Framebuffer(self.engine)
        self.normals       = bsk.Framebuffer(self.engine)
        self.dimensions    = bsk.Framebuffer(self.engine)

        # Level destinations
        self.plain = bsk.Framebuffer(self.engine)
        self.sight = bsk.Framebuffer(self.engine)

        # Post processes
        self.edge_detect = bsk.PostProcess(self.engine, 'shaders/edge_detect.frag')

        # Skys
        self.white_sky = bsk.Sky(self.engine, 'images/white.jpg')

        # Output vao        
        self.vbo = self.engine.ctx.buffer(np.array([[-1, -1, 0, 0, 0], [1, -1, 0, 1, 0], [1, 1, 0, 1, 1], [-1, 1, 0, 0, 1], [-1, -1, 0, 0, 0], [1, 1, 0, 1, 1]], dtype='f4'))
        self.vao = self.engine.ctx.vertex_array(self.output_shader.program, [(self.vbo, '3f 2f', 'in_position', 'in_uv')], skip_errors=True)
        
        # Edge detect combinations
        self.outline_combiner = self.engine.ctx.vertex_array(self.outline_combine_shader.program, [(self.vbo, '3f 2f', 'in_position', 'in_uv')], skip_errors=True)

        self.output_shader.program['dimensionMap'] = 0
        self.dimensions.texture.use(location=0)
        self.output_shader.program['plainView'] = 1
        self.plain.texture.use(location=1)
        self.output_shader.program['sightView'] = 2
        self.sight_prepass.texture.use(location=2)

        self.sight_shader.program['depthMap'] = 3
        self.dimensions.depth.use(location=3)
        self.game.particle_shader.program['depthMap'] = 4
        self.dimensions.depth.use(location=4)

        #Edge detect
        self.outline_combine_shader.program['baseOutline'] = 5
        self.edge_sight.texture.use(location=5)
        self.outline_combine_shader.program['otherOutline'] = 6
        self.edge_normal.texture.use(location=6)

        self.dim_shader.program['plainDepthTex'] = 7
        self.geometry.depth.use(location=7)

        # self.output_shader.program['dimDepthTex'] = 7
        # self.dimensions.depth.use(location=7)
        # self.output_shader.program['plainDepthTex'] = 8
        # self.normals.depth.use(location=8)

        self.show = self.geometry

    def update_scenes(self):
        """
        Updates the nessecary data in the scenes
        """
        self.game.plain_scene.node_handler.update()
        self.game.plain_scene.particle.update()
        self.game.dimension_scene.node_handler.update()
        self.game.dimension_scene.particle.update()
        self.game.sight_scene.node_handler.update()
        self.game.sight_scene.particle.update()
        if self.game.engine.delta_time < 0.5: # TODO this will cause physics to slow down when on low frame rate, this is probabl;y acceptable
            self.game.sight_scene.collider_handler.resolve_collisions()

    def render(self) -> None:
        """
        
        """
        
        self.update_scenes()

        # Render Geom
        self.engine.scene = self.game.plain_scene
        self.engine.shader = self.geo_shader
        self.game.plain_scene.sky = None
        self.game.plain_scene.render(self.geometry)

        # Render the dimesions map and depth
        self.engine.scene = self.game.dimension_scene
        self.engine.shader = self.dim_shader
        self.game.dimension_scene.sky = None
        self.game.dimension_scene.render(self.dimensions)
        
        self.dim_shader.program['plainDepthTex'] = 7
        self.geometry.depth.use(location=7)

        # Render the normals
        self.engine.scene = self.game.plain_scene
        self.engine.shader = self.norm_shader
        self.game.plain_scene.render(self.normals)

        # Render the sight scene with the dimensions depth
        self.engine.scene = self.game.sight_scene
        self.engine.shader = self.sight_shader
        self.game.plain_scene.sky = self.white_sky
        self.game.sight_scene.render(self.sight_prepass)

        # Edge detect
        self.edge_detect.apply(self.normals, self.edge_normal)
        self.edge_detect.apply(self.dimensions, self.edge_sight)
        self.outline_combine_shader.program['baseOutline'] = 5
        self.edge_sight.texture.use(location=5)
        self.outline_combine_shader.program['otherOutline'] = 6
        self.edge_normal.texture.use(location=6)
        self.plain.use()
        self.plain.clear()
        self.outline_combiner.render()



        # Show to the screen
        self.engine.ctx.screen.use()
        self.engine.ctx.clear()
        self.output_shader.program['dimensionMap'] = 0
        self.dimensions.texture.use(location=0)
        self.output_shader.program['plainView'] = 1
        self.plain.texture.use(location=1)
        self.output_shader.program['sightView'] = 2
        self.sight_prepass.texture.use(location=2)

        # TODO depth
        # self.output_shader.program['dimDepthTex'] = 7
        # self.dimensions.depth.use(location=7)
        # self.output_shader.program['plainDepthTex'] = 8
        # self.normals.depth.use(location=8)

        self.vao.render()
        
        # Render ui
        self.engine.ctx.disable(mgl.DEPTH_TEST)
        self.engine.scene = self.game.default_scene
        self.engine.shader = self.game.default_shader
        self.game.ui.render()
        self.game.default_scene.sky = None
        self.game.default_scene.render()
        self.engine.ctx.enable(mgl.DEPTH_TEST)
        # self.show.render()
        # pg.display.flip()


    def resize(self):
        # First render pass
        self.sight_prepass.resize()
        self.edge_sight.resize()
        self.edge_normal.resize()
        self.geometry.resize()
        self.normals.resize()
        self.dimensions.resize()

        # Level destinations
        self.plain.resize()
        self.sight.resize()

        # Post processes
        self.edge_detect.resize()