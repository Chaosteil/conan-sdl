#include <stdio.h>
#include <SDL.h>

int main() {
  if (SDL_Init(0)) return 1;
  SDL_Quit();
  return 0;
}
