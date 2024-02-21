export async function importImage(game: string): Promise<string> {
  const { default: image } = await import(`/logos/${game}.webp`);
  return image;
}