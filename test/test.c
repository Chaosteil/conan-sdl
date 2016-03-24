#include <stdio.h>
#include <SDL2/SDL.h>

int main() {
  if (SDL_Init(SDL_INIT_VIDEO)) return 1;
  SDL_Quit();
  return 0;
}
