from big_ol_pile_of_manim_imports import *

OUTPUT_DIRECTORY = "temperature"

def color(hot=0):
	cold_color = [0x58, 0xC4, 0xDD]
	hot_color = [0xff, 0x00, 0x00]
	if not (MIN_HOT <= hot <= MAX_HOT):
		print("please enter a value between 0 and 100")
		return False
	
	color = []
	for i in range(len(cold_color)):
		color.append(
			cold_color[i]
			+
			(hot_color[i] - cold_color[i]) * hot / 100
		)
	return '#' + ''.join("%02X"%int(i) for i in color)
MAX_HOT = MIN_COLD = 100
MIN_HOT = MAX_COLD = 0

def polar_to_3_array(r, theta=None):
	if theta is None:
		r, theta = r
	x,y = polar_to_cartesian(r, theta)
	return np.array((x, y, 0))

# 
# post 2
# 
class IntroduceGasParticles(Scene):
	CONFIG = {
		"random_seed": 2,
		"particles_config": [
			{
				"color": color(100),
				"point":           ORIGIN + 2*LEFT + 2*UP,
				"velocity":        3,
				"movement_radius": 2,
			},
			{
				"color": color(100),
				"point":           ORIGIN + 2*RIGHT + 2*UP,
				"velocity":        3,
				"movement_radius": 2,
			},
			{
				"color": color(50),
				"point":           ORIGIN + 2*LEFT + 2*DOWN,
				"velocity":        1,
				"movement_radius": 1,
			},
			{
				"color": color(50),
				"point":           ORIGIN + 2*RIGHT + 2*DOWN,
				"velocity":        1,
				"movement_radius": 1,
			},
			{
				"color": color(0),
				"point":           ORIGIN,
				"velocity":        0.4,
				"movement_radius": 0.5,
			},
		]
	}
	def construct(self):
		self.wait(0.2)

		# add random particles
		self.particles = [
			self.initiate_particle(**config)
			for config in self.particles_config
		]
		self.radiuses = [
			p.create_radius()
			for p in self.particles
		]
		self.add(*self.radiuses, *self.particles)
		self.play(
			*[
				Write(radius)
				for radius in self.radiuses
			]
		)

		self.resume_updating()
		self.wait(6)

	def initiate_particle(self, color=None, **kwargs):
		p = Particle2D(**kwargs)
		if color:
			p.set_color(color)
		p.add_updater(p.__class__.random_walk)
		p.suspend_updating()
		return p

	def suspend_updating(self):
		for m in self.mobjects:
			m.suspend_updating()

	def resume_updating(self):
		for m in self.mobjects:
			m.resume_updating()

class CollideToGas(Scene):
	CONFIG = {
		"random_seed": 2,
		"stage_A": { # initial. let the random motion begin
			"p_cold": {
				"locations": [
					(0.25, 270*DEGREES),
					(0.25, 320*DEGREES),
					(0.5 , 130*DEGREES), # collision
					(0.4 , 35 *DEGREES),
				],
				"config": {
					"point":           ORIGIN + 1*RIGHT + 2*DOWN,
					"velocity":        1,
					"movement_radius": 0.5,
				},
				"color": color(MIN_HOT),
			},
			"p_hot_1": {
				"locations": [
					(1, 240*DEGREES),
					(3, 305*DEGREES), # collision
				],
				"config": {
					"point":           ORIGIN + (-1)*RIGHT + 1*UP,
					"velocity":        3,
					"movement_radius": 3,
				},
				"color": color(MAX_HOT),
			},
			"p_hot_2": {
				"locations": [
					(1  , 20 *DEGREES),
					(2.2, 174*DEGREES),
					(1.5, 74 *DEGREES),
					(1.8, 220*DEGREES),
					(1.3, 40 *DEGREES),
					(2.6, 254*DEGREES), # collision
					(1.5, 85 *DEGREES),
				],
				"config": {
					"point":           ORIGIN + 2*RIGHT + 1*UP,
					"velocity":        3,
					"movement_radius": 3,
				},
				"color": color(MAX_HOT),
			},
			"circle": {
				"arc_center": 0.65*RIGHT + 1.5*DOWN,
				"radius": 0.4,
			},
			"duration": 1.2,
		},
		"stage_B": { # after cold & hot_1 collide
			"p_cold": {
				"locations": [
					(0.4 , 20 *DEGREES),
					(0.25, 210*DEGREES),
					(0.6 , 60 *DEGREES), # collision
					(0.4 , 35 *DEGREES),
				],
				"config": {
					"point":           ORIGIN + 1*RIGHT + 2*DOWN,
					"velocity":        1.7,
					"movement_radius": 0.7,
				},
				"color": color(25),
			},
			"p_hot_1": {
				"locations": [], # random walk
				"config": {
					"point":           ORIGIN + 1*RIGHT + 1*UP,
					"velocity":        2.4,
					"movement_radius": 3,
				},
				"color": color(75),
			},
			"circle": {
				"arc_center": 1.22*RIGHT + 1.57*DOWN,
				"radius": 0.4,
			},
			"duration": 4.42,
		},
		"stage_C": { # after cold & hot_2 collide
			"p_cold": {
				"locations": [], # random walk
				"config": {
					# moving it upward, to the gas location
					"point":           ORIGIN + 1*RIGHT + 2*UP,
					"velocity":        2.5,
					"movement_radius": 2.5,
				},
				"color": color(75),
			},
			"p_hot_2": {
				"locations": [], # random walk
				"config": {
					"point":           ORIGIN + 2*RIGHT + 1*UP,
					"velocity":        2.4,
					"movement_radius": 3,
				},
				"color": color(75),
			},
			"duration": 6,
		},
		"random_particles_config": {
			"cold": {
				"config": {
					"velocity":        1,
					"movement_radius": 0.5,
				},
				"color": color(MIN_HOT),
				"points": [ # left to right, our special one in the middle
					ORIGIN + 7  *LEFT  + 1.9*DOWN,
					ORIGIN + 6.6*LEFT  + 3.4*DOWN,
					ORIGIN + 6.1*LEFT  + 2.5*DOWN,
					ORIGIN + 6  *LEFT  + 1.9*DOWN,
					ORIGIN + 5.6*LEFT  + 2.9*DOWN,
					ORIGIN + 5  *LEFT  + 1.9*DOWN,
					ORIGIN + 4.7*LEFT  + 3.3*DOWN,
					ORIGIN + 4.5*LEFT  + 2.5*DOWN,
					ORIGIN + 4  *LEFT  + 1.9*DOWN,
					ORIGIN + 4.2*LEFT  + 2.8*DOWN,
					ORIGIN + 3.7*LEFT  + 3.1*DOWN,
					ORIGIN + 3.3*LEFT  + 2.5*DOWN,
					ORIGIN + 3  *LEFT  + 1.9*DOWN,
					ORIGIN + 2.8*LEFT  + 3.1*DOWN,
					ORIGIN + 2.5*LEFT  + 2.6*DOWN,
					ORIGIN + 2.2*LEFT  + 2.1*DOWN,
					ORIGIN + 2  *LEFT  + 3.2*DOWN,
					ORIGIN + 1.8*LEFT  + 1.6*DOWN,
					ORIGIN + 1.5*LEFT  + 2.4*DOWN,
					ORIGIN + 1.4*LEFT  + 3.3*DOWN,
					ORIGIN + 0.9*LEFT  + 1.9*DOWN,
					ORIGIN + 0.7*LEFT  + 2.3*DOWN,
					ORIGIN + 0.2*LEFT  + 3.1*DOWN,
					ORIGIN + 0.1*RIGHT + 1.8*DOWN,
					ORIGIN + 0.5*RIGHT + 3.3*DOWN,
					ORIGIN + 0.7*RIGHT + 2.5*DOWN,
					# ORIGIN + 1*RIGHT + 2*DOWN
					ORIGIN + 1.4*RIGHT + 2.6*DOWN,
					ORIGIN + 1.7*RIGHT + 3.3*DOWN,
					ORIGIN + 2  *RIGHT + 2  *DOWN,
					ORIGIN + 2.4*RIGHT + 1.9*DOWN,
					ORIGIN + 2.7*RIGHT + 2.4*DOWN,
					ORIGIN + 2.9*RIGHT + 3.4*DOWN,
					ORIGIN + 3.3*RIGHT + 2.5*DOWN,
					ORIGIN + 3.4*RIGHT + 1.7*DOWN,
					ORIGIN + 3.6*RIGHT + 3.3*DOWN,
					ORIGIN + 3.7*RIGHT + 1.7*DOWN,
					ORIGIN + 4  *RIGHT + 1.7*DOWN,
					ORIGIN + 4.1*RIGHT + 3.1*DOWN,
					ORIGIN + 4.5*RIGHT + 2.5*DOWN,
					ORIGIN + 4.7*RIGHT + 1.9*DOWN,
					ORIGIN + 5  *RIGHT + 2.3*DOWN,
					ORIGIN + 5.1*RIGHT + 3.3*DOWN,
					ORIGIN + 5.2*RIGHT + 1.9*DOWN,
					ORIGIN + 5.5*RIGHT + 2.4*DOWN,
					ORIGIN + 5.7*RIGHT + 2.8*DOWN,
					ORIGIN + 6  *RIGHT + 1.7*DOWN,
					ORIGIN + 6.1*RIGHT + 3.1*DOWN,
					ORIGIN + 6.4*RIGHT + 2.5*DOWN,
					ORIGIN + 7  *RIGHT + 1.7*DOWN,
				]
			},
			"hot": {
				"config": {
					"velocity":        3,
					"movement_radius": 3,
				},
				"color": color(MAX_HOT),
				"points": [ # left to right, our special one in the middle
					ORIGIN + 6.5*LEFT  + 2.4*UP,
					ORIGIN + 5.7*LEFT  + 2.4*UP,
					ORIGIN + 4.8*LEFT  + 2.2*UP,
					ORIGIN + 4  *LEFT  + 2  *UP,
					ORIGIN + 3.1*LEFT  + 1.7*UP,
					ORIGIN + 2  *LEFT  + 2.1*UP,
					ORIGIN + 0.1*RIGHT + 2.3*UP,
					# ORIGIN + (-1)*RIGHT + 1*UP
					# ORIGIN + 2*RIGHT + 1*UP
					ORIGIN + 2.8*RIGHT + 2.5*UP,
					ORIGIN + 3  *RIGHT + 1.5*UP,
					ORIGIN + 3.5*RIGHT + 2  *UP,
					ORIGIN + 4.3*RIGHT + 2.2*UP,
					ORIGIN + 5  *RIGHT + 1.5*UP,
					ORIGIN + 5.1*RIGHT + 2.5*UP,
					ORIGIN + 5.9*RIGHT + 1.5*UP,
					ORIGIN + 6.5*RIGHT + 2.5*UP,
					ORIGIN + 7.3*RIGHT + 2.2*UP,
				]
			},
		}
	}
	def construct(self):
		self.wait(0.2)

		# add random particles
		self.random_particles = []
		for group in self.random_particles_config:
			for point in self.random_particles_config[group]["points"]:
				p = self.initiate_particle(
					color=self.random_particles_config[group]["color"],
					point=point,
					**self.random_particles_config[group]["config"],
				)
				self.random_particles.append(p)
		self.add(*self.random_particles)

		# create stage A
		self.stage_A_particles = self.initiate_stage("stage_A")
		self.latest_particles = list(self.stage_A_particles)
		self.add(*self.stage_A_particles)

		self.wait(2)
		self.run_stage("stage_A")
		self.mark_stage("stage_A")

		# p_cold, p_hot_1, p_hot_2 = self.transform_to_new_stage("stage_B")
		self.stage_B_particles = self.transform_to_new_stage("stage_B")
		self.run_stage("stage_B")
		self.mark_stage("stage_B")

		# p_cold, p_hot_1, p_hot_2 = self.transform_to_new_stage("stage_C")
		self.stage_C_particles = self.transform_to_new_stage("stage_C")
		self.run_stage("stage_C")
		self.wait()

	def initiate_stage(self, stage_name):
		stage_data = self.__dict__[stage_name]

		if "p_cold" in stage_data:
			p_cold_data = stage_data["p_cold"]
			p_cold = self.initiate_particle(
				color=p_cold_data["color"],
				# config
				**p_cold_data["config"],
				location_list=self._generate_location_list(p_cold_data["locations"])
			)
		else:
			p_cold = None


		if "p_hot_1" in stage_data:
			p_hot_1_data = stage_data["p_hot_1"]
			p_hot_1 = self.initiate_particle(
				color=p_hot_1_data["color"],
				# config
				**p_hot_1_data["config"],
				location_list=self._generate_location_list(p_hot_1_data["locations"])
			)
		else:
			p_hot_1 = None

		if "p_hot_2" in stage_data:
			p_hot_2_data = stage_data["p_hot_2"]
			p_hot_2 = self.initiate_particle(
				color=p_hot_2_data["color"],
				# config
				**p_hot_2_data["config"],
				location_list=self._generate_location_list(p_hot_2_data["locations"])
			)
		else:
			p_hot_2 = None

		return p_cold, p_hot_1, p_hot_2

	def run_stage(self, stage_name):
		self.resume_updating()
		self.wait(self.__dict__[stage_name]["duration"])
		self.suspend_updating()

	def mark_stage(self, stage_name):
		c = Circle( **self.__dict__[stage_name]["circle"] )
		self.add(c)
		self.play(Write(c))
		self.play(FadeOut(c))
		self.remove(c)

	def transform_to_new_stage(self, stage_name):
		particles = self.initiate_stage(stage_name)
		for i in range(len(particles)):
			if particles[i] is not None:
				self.inherit_location(particles[i], self.latest_particles[i])
		# self.inherit_location(p_cold, self.p_cold)
		# self.inherit_location(p_hot_1, self.p_hot_1)
		# self.inherit_location(p_hot_2, self.p_hot_2)
		self.play(
			# ReplacementTransform is used so that self.p will get the new location_list,
			# ReplacementTransform(self.p_cold, p_cold),
			# ReplacementTransform(self.p_hot_1, p_hot_1),
			# ReplacementTransform(self.p_hot_2, p_hot_2),
			*[
				ReplacementTransform(self.latest_particles[i], particles[i])
				for i in range(len(particles))
				if particles[i] is not None
			]
		)
		for i in range(len(particles)):
			if particles[i] is not None:
				self.latest_particles[i] = particles[i]
		return particles

	def inherit_location(self, p_new, p_old):
		p_new.move_to(p_old.get_center())

	def initiate_particle(self, color=None, **kwargs):
		p = Particle2D(**kwargs)
		if color:
			p.set_color(color)
		p.add_updater(p.__class__.random_walk)
		p.suspend_updating()
		return p

	def _generate_location_list(self, l):
		return list(map(polar_to_3_array, l))

	def suspend_updating(self):
		for m in self.mobjects:
			m.suspend_updating()

	def resume_updating(self):
		for m in self.mobjects:
			m.resume_updating()



class MeltIce(Scene):
	CONFIG = {
		"crystal_config": {
			"theta": 45*DEGREES,
			"distance_between_particles": 0.4,
			"y_max": 0,

			"particle_config": {
				"movement_radius": 0.3,
				"velocity": 0.1,
			},
		},

		"line_height": 0,
		"squash_factor": 0.7,
		"amount_of_steps": 4,
	}
	def construct(self):
		self.wait(0.2)

		line = Line(
			start= self.camera.get_frame_width()*LEFT + self.line_height*UP,
			end  =-self.camera.get_frame_width()*LEFT + self.line_height*UP,
		)
		self.add(line)
		self.play(Write(line))

		crystal = Crystal(**self.crystal_config)
		crystal.set_color(BLUE)
		self.add(crystal)

		self.play(*crystal.write_simultaneously(), suspend_mobject_updating=False)
		self.play(*crystal.write_radius_simultaneously())

		self.particles_by_height = particles_by_height = crystal.get_particles_by_height()
		self.heights = heights = list(particles_by_height.keys())
		heights.sort(reverse=True)

		crystal.resume_updating()
		self.wait(3)

		for n in range(self.amount_of_steps):
			crystal.suspend_updating()
			self._step_n(n+1)
			crystal.resume_updating()
			self.wait(3)

		self.wait(3)

	def squash(self):
		"""
		lower line at line_velocity
		if line is at heighest particle layer - start squashing the layers

		squash:
			step 1:
				for the top layer:
					reduce movement_radius by a factor of 0.7
					move initial_position accordingly
					move line accordingly
					increase the velocity by a factor of 1/0.7
					increase particles color
				total movement:
					(1 - 0.7) * step_x
			step_2:
				for the first 2 layers:
					same as step 1
					now, the top layer will have its movement radius reduced
					  (from the original) by a factor of 0.7^2
					and the velocity higher by a factor of 0.7^2
				total movement:
					from layer 1: (0.7 - 0.7^2) * step_x
					from layer 2: (1   - 0.7  ) * step_x

			line speed ~~ 0.7^step
			layer_n radius = movement_radius * 0.7^(step - n)
				n is layer number, zero based
				step-n >= 0
			layer_n velocity = velocity * 1 / radius_factor
		"""
		pass

	def _step_n(self, n):
		factor = self.squash_factor
		color_per_step = MAX_HOT / (self.amount_of_steps)
		radius = self.crystal_config["distance_between_particles"] or self.crystal_config["particle_config"]["movement_radius"]

		for i in range(n):
			# calculate layer color
			layer_color = color_per_step * (n - i)
			if layer_color < MIN_HOT:
				layer_color = MIN_HOT
			layer_color = color(layer_color)

			layer_y_change = 0
			for j in range(i+1, n):
				# j is the layer
				l = n - j
				print(f"    n={n}, i={i}, j={j}, l={l}, addition={factor**(l-1) - factor**(l)}")
				layer_y_change += factor**(l-1) - factor**(l)
			print(f"step {n}: layer {i+1} is moved by {layer_y_change}")
			layer_y_change *= radius

			# squash layer i
			for p in self.particles_by_height[self.heights[i]]:
				# set new initial position
				old_initial_y = p.initial_position[1]
				old_radius = p.movement_radius
				new_radius = old_radius * factor
				new_initial_y = old_initial_y - old_radius + new_radius
				new_initial_y -= layer_y_change
				p.initial_position[1] = new_initial_y
				# update velocity
				p.velocity /= 0.7
				# update radius
				p.movement_radius *= 0.7

				# update surrounding circle
				# circle.stretch(factor, dim, **kwargs)
				p.radius_mobject.stretch(0.7, 1)
				p.radius_mobject.shift((new_radius - old_radius) * UP)
				p.radius_mobject.shift(layer_y_change * DOWN)

				p.set_color(layer_color)

				"""
				save each parameter as initial_state and final_state
					initial_y_position
					velocity
					movement_radius
					radius_mobject.stretch amount
					radius_mobject.shift amount
					color
				they all grow linearly
				set run_time = factor^(-n)
				then play by amount
					where amount = dt / run_time

				plus, add line movement
				"""


		# line_velocity /= 0.7
		pass

class Ice(Scene):
	CONFIG = {
		"crystal_config": {
			"theta": 45*DEGREES,
			"distance_between_particles": 0.3,
			"x_max":  1,
			"x_min": -1,
			"y_max":  1,
			"y_min": -1,

			"particle_config": {
				"movement_radius": 0.05,
				"velocity": 0.1,
			},
		},
	}
	def construct(self):
		self.wait(0.2)

		crystal = Crystal(**self.crystal_config)
		crystal.set_color("#A5F2F3")
		self.add(crystal)

		self.play(*crystal.write_simultaneously(), suspend_mobject_updating=False)
		# self.play(*crystal.write_radius_simultaneously())

		self.wait(1.5)
		crystal.resume_updating()
		self.wait(12)


# 
# post 1
# 
class ShootParticles(Scene):
	CONFIG = {
		"q": 1,
		"E": Y_AXIS,
		"B": Z_AXIS,

		"particles": [
			# (v, color, mass)
			(1.3, RED_C   , 1),
			(1  , YELLOW_E, 1.6),
			(0.6, BLUE_D  , 1),
			(2  , RED_E   , 1),
			(1  , YELLOW_D, 0.8),
			(0.2, BLUE_E  , 1),
			(1  , YELLOW_C, 0.4),
			(1.6, RED_D   , 1),
		],

		"laser_tip_position": 3*LEFT,
		"laser_base_width"  : 4,
		"laser_height"      : 1,
		"laser_color"       : WHITE,
		"wall_position"     : 5*RIGHT,
		"wall_width"        : 0.2,
		"wall_opening"      : 0.25,

		"run_time": 16,

		"draw"          : False,
		"shoot_together": True,
		"show_force_1"  : True,
		"show_force_2"  : True,
	}
	def construct(self):
		self.wait(0.2)
		self.initiate_stage()
		for v, color, mass in self.particles:
			self.shoot_single(color=color, mass=mass, velocity=v*RIGHT)
		self.wait(self.run_time)

	def initiate_stage(self):
		"""
		display laser
		display laser text
		display wall
		display wall text
		display E & B
		"""
		# laser
		laser_base_center = self.laser_tip_position + (1/np.cos(np.pi/6))  *LEFT + self.laser_base_width/2*LEFT
		laser_base_center += 0.1 * RIGHT
		laser_base = Rectangle(
			width =self.laser_base_width,
			height=self.laser_height,
			color=self.laser_color,
		).move_to(laser_base_center)
		laser_base.set_fill(opacity=1)

		laser_tip_center = self.laser_tip_position + (1/np.cos(np.pi/6))/2*LEFT
		laser_tip = Triangle(
			start_angle = np.pi/3,
			color=self.laser_color,
		).flip().set_height(self.laser_height).move_to(laser_tip_center)
		laser_tip.set_fill(opacity=1)

		laser_text = TextMobject("particle gun")
		laser_text.next_to(laser_base, UP, buff = 0)
		laser_text.shift(0.2*UP + 0.5*RIGHT)

		wall_top = Line(
			start=self.wall_position + self.wall_opening/2*UP,
			end  =self.wall_position + 10*UP,
		)
		wall_bottom = Line(
			start=self.wall_position + self.wall_opening/2*DOWN,
			end  =self.wall_position + 10*DOWN,
		)

		E_left  = TexMobject("\\vec{E}=1\\hat{y}")
		B_left  = TexMobject("\\vec{B}=1\\hat{z}")
		E_right = TexMobject("\\vec{E}=0\\hat{y}")
		B_right = TexMobject("\\vec{B}=1\\hat{z}")

		E_left.next_to (wall_top, LEFT )
		E_left.shift(1.5*DOWN)
		B_left.next_to (E_left  , DOWN , buff=0.1)

		E_right.next_to(wall_top, RIGHT)
		E_right.shift(1.5*DOWN)
		B_right.next_to(E_right , DOWN , buff=0.1)

		self.add(
			laser_base, laser_tip, laser_text,
			wall_top, wall_bottom,
			E_left, B_left, E_right, B_right,
		)

	def shoot_single(self, color, *args, **kwargs):
		if self.draw:
			self.suspend_updating()
		self.add_single(color=color, *args, **kwargs)
		if self.draw:
			self.resume_updating()
		if not self.shoot_together:
			self.wait()

	def add_single(self, color, *args, **kwargs):
		# initiate particle
		p = ChargedParticle(
			q=self.q,
			E=self.E,
			B=self.B,
			point=self.laser_tip_position,
			*args,
			**kwargs
		)
		p.set_color(color)
		p.color = color
		# show particle
		self.add(p)
		if self.draw:
			self.play(Write(p))

		# initiate force arrow
		if self.show_force_1:
			p.init_force_arrow()
			p.force_arrow.set_color(color)
			self.add(p.force_arrow)
			if self.draw:
				self.play(Write(p.force_arrow))

		# add updaters
		p.add_updater(p.__class__.walk_by_force)
		if self.show_force_1:
			p.add_updater(p.__class__.update_force_arrow)
		self.add_trajectory(p, color)

		# add wall related updaters
		wall_x = self.wall_position[0]
		wall_y = self.wall_opening / 2
		# an updater to stop particles who collide with the wall
		# and, for the particle that passes through - change its dynamics into magnetic field only
		def interact_with_wall(particle, dt):
			# particles will come from the left
			if particle.get_x() >= wall_x:
				if abs(particle.get_y()) >= wall_y:
					particle.suspend_updating()
				else:
					particle.E = 0*UP
					# particle.E = np.array((0., 0., 4))
					particle.remove_updater(interact_with_wall)
					particle.add_updater(interact_with_wall_2)

					if self.show_force_2:
						particle.init_force_arrow()
						particle.force_arrow.set_color(particle.color)
						self.add(particle.force_arrow)
						particle.add_updater(particle.__class__.update_force_arrow)
		def interact_with_wall_2(particle, dt):
			# particles will come from the right
			if particle.get_x() <= wall_x:
				particle.suspend_updating()
		p.add_updater(interact_with_wall)

		return p

	def add_trajectory(self, p, color):
		def update_trajectory(traj, dt):
			new_point = traj.p.get_center()
			if get_norm(new_point - traj.points[-1]) > 0.01:
				traj.add_smooth_curve_to(new_point)

		traj = VMobject()
		traj.set_color(color)
		traj.p = p
		# traj.start_new_path(p.point)
		traj.start_new_path(p.get_center())
		traj.set_stroke(p.color, 1, opacity=0.75)
		traj.add_updater(update_trajectory)
		self.add(traj, p)


	def suspend_updating(self):
		for m in self.mobjects:
			m.suspend_updating()

	def resume_updating(self):
		for m in self.mobjects:
			m.resume_updating()

class ShootParticles_OneByOne(ShootParticles):
	CONFIG = {
		"draw"          : True,
		"shoot_together": False,
		"run_time": 9,
	}
class ShootParticles_OneByOne_Quick(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": False,
		"run_time": 9,
	}
class ShootParticles_Together(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": True,
		"run_time": 15,
	}
class ShootParticles_Together_Full(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": True,

		"wall_opening"      : 0.2,
		"particles": [
			# (v, color, mass)
			(1.1, RED_C   , 1),
			(1.2, RED_C   , 1),
			(1.3, RED_C   , 1),
			(1.4, RED_C   , 1),
			(1.5, RED_C   , 1),
			(1.6, RED_C   , 1),
			(1.7, RED_C   , 1),
			(1.8, RED_C   , 1),
			(1.9, RED_C   , 1),
			(2.0, RED_C   , 1),

			(1  , YELLOW_E, 0.2),
			(1  , YELLOW_E, 0.4),
			(1  , YELLOW_E, 0.6),
			(1  , YELLOW_E, 0.8),
			(1  , YELLOW_E, 1.0),
			(1  , YELLOW_E, 1.2),
			(1  , YELLOW_E, 1.4),
			(1  , YELLOW_E, 1.6),
			(1  , YELLOW_E, 1.8),

			(0.1, BLUE_C  , 1),
			(0.2, BLUE_C  , 1),
			(0.3, BLUE_C  , 1),
			(0.4, BLUE_C  , 1),
			(0.5, BLUE_C  , 1),
			(0.6, BLUE_C  , 1),
			(0.7, BLUE_C  , 1),
			(0.8, BLUE_C  , 1),
			(0.9, BLUE_C  , 1),
		],
	}
class ShootParticles_Together_VeryFull(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": True,

		"wall_opening"      : 0.2,
		"particles": [
			# (v, color, mass)
			(1.1, RED_C   , 1),
			(1.2, RED_C   , 1),
			(1.3, RED_C   , 1),
			(1.4, RED_C   , 1),
			(1.5, RED_C   , 1),
			(1.6, RED_C   , 1),
			(1.7, RED_C   , 1),
			(1.8, RED_C   , 1),
			(1.9, RED_C   , 1),
			(2.0, RED_C   , 1),
			(2.1, RED_C   , 1),
			(2.2, RED_C   , 1),
			(2.3, RED_C   , 1),
			(2.4, RED_C   , 1),
			(2.5, RED_C   , 1),
			(2.6, RED_C   , 1),
			(2.7, RED_C   , 1),
			(2.8, RED_C   , 1),
			(2.9, RED_C   , 1),
			(3.0, RED_C   , 1),

			(1  , YELLOW_E, 0.2),
			(1  , YELLOW_E, 0.4),
			(1  , YELLOW_E, 0.6),
			(1  , YELLOW_E, 0.8),
			(1  , YELLOW_E, 1.0),
			(1  , YELLOW_E, 1.2),
			(1  , YELLOW_E, 1.4),
			(1  , YELLOW_E, 1.6),
			(1  , YELLOW_E, 1.8),

			(0.1, BLUE_C  , 1),
			(0.2, BLUE_C  , 1),
			(0.3, BLUE_C  , 1),
			(0.4, BLUE_C  , 1),
			(0.5, BLUE_C  , 1),
			(0.6, BLUE_C  , 1),
			(0.7, BLUE_C  , 1),
			(0.8, BLUE_C  , 1),
			(0.9, BLUE_C  , 1),
		],
	}
class ShootParticles_Together_Full_NoForce2(ShootParticles_Together_Full):
	CONFIG = {
		"show_force_2"    : False,
	}
class ShootParticles_Together_Full_NoForce(ShootParticles_Together_Full):
	CONFIG = {
		"show_force_1"    : False,
		"show_force_2"    : False,
	}
class ShootParticles_Together_VeryFull_NoForce(ShootParticles_Together_VeryFull):
	CONFIG = {
		"show_force_1"    : False,
		"show_force_2"    : False,
	}
class ShootParticles_Extruder(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": True,
		"show_force_1"    : False,
		"show_force_2"    : False,

		"wall_opening"      : 0.25,
		"particles": [
			# (v, color, mass)
			(1.6, RED_E   , 1),
			(1.1, RED_C   , 1),

			(1  , YELLOW_E, 0.4),
			(1  , YELLOW_E, 0.8),
			(1  , YELLOW_C, 1),
			(1  , YELLOW_E, 1.6),

			(0.95, BLUE_C  , 1),
			(0.4 , BLUE_E  , 1),
		],
	}
class ShootParticles_test(ShootParticles):
	CONFIG = {
		"draw"          : False,
		"shoot_together": True,
		"show_force_1"    : False,
		"show_force_2"    : False,

		"wall_opening"      : 0.25,
		"particles": [
		],
	}


# 
# post 3
# 
class Box(object):
	CONFIG = {
	}
	def construct(self):
		self.wait(0.2)
		c = Crystal()
		

# 
# playground
# 
class IntroduceVectorField(Scene):
	CONFIG = {
		"coordinate_plane_config": {
			"y_line_frequency": PI / 2,
			# "x_line_frequency": PI / 2,
			"x_line_frequency": 1,
			"y_axis_config": {
				# "unit_size": 1.75,
				"unit_size": 1,
			},
			"y_max": 4,
			"faded_line_ratio": 4,
			"background_line_style": {
				"stroke_width": 1,
			},
		},
		"initial_grid_wait_time": 15,
		"vector_field_config": {
			"max_magnitude": 3,
			# "delta_x": 2,
			# "delta_y": 2,
		},
	}

	def construct(self):
		plane = self.initialize_plane()
		self.add(plane)
		self.initialize_vector_field()
		self.preview_vector_field()
		self.show_full_vector_field()

	def initialize_plane(self):
		plane = self.plane = NumberPlane(
			**self.coordinate_plane_config
		)
		plane.y_axis.add_numbers(direction=DL)
		plane.x_axis.add_numbers(direction=DL)
		return plane

	def initialize_vector_field(self):
		self.vector_field = VectorField(
			self.vector_field_func,
			**self.vector_field_config,
		)
		self.vector_field.sort(get_norm)

	def preview_vector_field(self):
		vector_field = self.vector_field

		growth = LaggedStartMap(
			GrowArrow, vector_field,
			run_time=3,
			lag_ratio=0.01,
		)
		self.add(
			growth.mobject,
			vector_field,
		)

		self.play(growth)
		self.wait()
		self.play(FadeOut(vector_field))
		self.remove(growth.mobject)

	def show_full_vector_field(self):
		vector_field = self.vector_field
		
		growth = LaggedStartMap(
			GrowArrow, vector_field,
			run_time=3,
			lag_ratio=0.01,
		)
		self.add( growth.mobject )
		self.play( growth )

	#
	def vector_field_func(self, point):
		x, y = self.plane.point_to_coords(point)

		return np.array([
			np.sign(x),
			np.sign(y),
			0,
		])

class ShowFlow(IntroduceVectorField):
	CONFIG = {
		"coordinate_plane_config": {
			"x_axis_config": {
				"unit_size": 0.8,
			},
			"x_max": 9,
			"x_min": -9,
		},
		"flow_time": 20,
	}

	def construct(self):
		self.initialize_plane()
		self.initialize_vector_field()
		plane = self.plane
		field = self.vector_field
		self.add(plane, field)

		stream_lines = StreamLines(
			field.func,
			delta_x=1,
			delta_y=1,
		)
		animated_stream_lines = AnimatedStreamLines(
			stream_lines,
			line_anim_class=ShowPassingFlashWithThinningStrokeWidth,
		)

		self.add(animated_stream_lines)
		self.wait(self.flow_time)
