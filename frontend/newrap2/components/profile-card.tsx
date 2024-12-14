import { motion } from 'framer-motion'
import Image from 'next/image'

interface ProfileCardProps {
  type: string
  username: string
  contributions: number
}

const cardImages = {
  'pr-manager': '/1734055610010.png',
  'fleet-master': '/1734055771105.png',
  'c3po': '/1734055868355.png',
  'contributor': '/1734055416172.png',
  'maintainer': '/1734055702717.png',
  'developer-pro': '/1734055343215.png',
  'learning': '/1734055358843.png',
  'real-deal': '/1734055502752.png',
}

export function getProfileCardType(contributions: number): string {
  if (contributions >= 1000) return 'real-deal'
  if (contributions >= 750) return 'developer-pro'
  if (contributions >= 500) return 'fleet-master'
  if (contributions >= 400) return 'pr-manager'
  if (contributions >= 300) return 'maintainer'
  if (contributions >= 200) return 'c3po'
  if (contributions >= 100) return 'contributor'
  return 'learning'
}

export default function ProfileCard({ type, username, contributions }: ProfileCardProps) {
  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="relative w-full max-w-md mx-auto mb-8"
    >
      <Image
        src={cardImages[type as keyof typeof cardImages]}
        alt={`${type} card`}
        width={400}
        height={200}
        className="w-full h-auto rounded-lg shadow-2xl"
      />
      <div className="absolute bottom-4 left-0 right-0 text-center text-white">
        <h3 className="text-xl font-bold">{username}</h3>
        <p className="text-sm opacity-80">{contributions} contributions</p>
      </div>
    </motion.div>
  )
}

