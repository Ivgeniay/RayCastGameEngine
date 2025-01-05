import math

# NOTE: game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
PENTA_HEIGHT = 5 * HEIGHT
DOUBLE_HEIGHT = 2 * HEIGHT
FPS = 60
TILE = 100

# NOTE: ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 4
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 2 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# из подобия трегольников H/D = h/d => h = H * d / D, где D - рассояние от игрока до стены,
# H - высота стены, d - расстояние от игрока до проекции стены на экране, h - высота проекции стены на экране
# h = H * d / D => h = H * TILE / D
# H == TILE, d = NUM_RAYS/(2 * tg(FOV/2)), D = depth

# NOTE: player settings
PLAYER_START_POS = (HALF_WIDTH, HALF_HEIGHT)
PLAYER_START_ANGLE = math.pi * 1.5
PLAYER_SPEED = 2
PLAYER_ROTATION_SPEED = 0.02
PLAYER_COLLISION_RADIUS = 20

# NOTE: controll settings
MOUSE_SENS = 0.001

# NOTE: sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS

# NOTE: textures settings
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# NOTE: map settings
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE = 2 * MINIMAP_SCALE
MAP_TILE = TILE // MAP_SCALE
MAP_POSITION = (0, 0)
MAP_PLAYER_RAY_LENGTH = 40
MAP_PLAYER_INDICATOR_RADIUS = 5

# NOTE: colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
YELLOW = (220, 220, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)
PURPLE = (120, 0, 120)
CYAN = (0, 120, 120)
ORANGE = (220, 120, 0)
SKYBLUE = (0, 186, 255)
SANDY = (244, 164, 96)
DARKBROWN = (100, 140, 0)
DARKORANGE = (255, 140, 0)
