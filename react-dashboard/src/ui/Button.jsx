import { cn } from './cn'
import { Spinner } from './Spinner'

const variantClasses = {
  primary:   'bg-primary text-on-primary hover:bg-primary-hover active:bg-primary-active border-transparent',
  secondary: 'bg-surface text-text border-border hover:bg-surface-muted active:bg-bg',
  ghost:     'bg-transparent text-text border-transparent hover:bg-surface-muted active:bg-bg',
  danger:    'bg-danger-solid text-white border-transparent hover:opacity-90 active:opacity-100',
}

const sizeClasses = {
  sm: 'h-control-sm px-3 text-sm gap-1.5',
  md: 'h-control-md px-4 text-base gap-2',
  lg: 'h-control-lg px-5 text-lg gap-2',
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  leftIcon: LeftIcon,
  rightIcon: RightIcon,
  fullWidth = false,
  children,
  className,
  disabled,
  type = 'button',
  onClick,
  ...props
}) {
  const isDisabled = disabled && !loading
  const handleClick = loading
    ? (e) => { e.preventDefault() }
    : onClick

  return (
    <button
      type={type}
      disabled={isDisabled}
      aria-disabled={disabled || loading || undefined}
      aria-busy={loading || undefined}
      onClick={handleClick}
      className={cn(
        'inline-flex items-center justify-center font-semibold rounded border',
        'transition-colors duration-fast',
        'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus-ring',
        disabled && !loading && 'opacity-40 cursor-not-allowed',
        loading && 'cursor-progress',
        variantClasses[variant],
        sizeClasses[size],
        fullWidth && 'w-full',
        className
      )}
      {...props}
    >
      {loading ? (
        <>
          <Spinner size={size === 'lg' ? 'md' : 'sm'} />
          <span>{children}</span>
        </>
      ) : (
        <>
          {LeftIcon && <LeftIcon size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} aria-hidden />}
          <span>{children}</span>
          {RightIcon && <RightIcon size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} aria-hidden />}
        </>
      )}
    </button>
  )
}
