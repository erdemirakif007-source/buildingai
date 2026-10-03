import { cn } from './cn'

const sizeClasses = {
  sm: 'w-3 h-3 border-[1.5px]',
  md: 'w-5 h-5 border-2',
  lg: 'w-7 h-7 border-[3px]',
}

export function Spinner({ size = 'md', className }) {
  return (
    <span
      role="status"
      aria-label="Yükleniyor"
      className={cn(
        'inline-block rounded-full border-current border-r-transparent animate-spin',
        sizeClasses[size],
        className
      )}
    />
  )
}
