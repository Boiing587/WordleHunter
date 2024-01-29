import Rand from 'rand-seed'
import Monster from '../interfaces/monster'
import { monsterList } from '../data/monsterList'

export default function getMonsterOfTheDay(): Monster | null {
  let seed = new Date().toDateString()
  if (!monsterList) { return null }
  return monsterList[ monsterList.length * new Rand(seed).next() << 0 ]
}