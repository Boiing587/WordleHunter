export default interface Monster {
  name: string
  species: string
  subspecies: string
  generation: string
  game: string
  elements?: string[]
  statuses?: string[]
  weaknesses?: string[]
}