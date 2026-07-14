import { forwardRef } from 'react';
import { clsx } from 'clsx';

const variants = {
  default: 'bg-[var(--primary)] text-white hover:bg-[var(--primary)]/90 shadow-sm hover:shadow-md',
  outline: 'border border-[var(--border)] bg-transparent hover:bg-[var(--secondary)] text-[var(--foreground)]',
  ghost: 'bg-transparent hover:bg-[var(--secondary)] text-[var(--foreground)]',
  destructive: 'bg-[var(--destructive)] text-white hover:bg-[var(--destructive)]/90',
  gold: 'btn-gold',
  link: 'text-[var(--primary)] underline-offset-4 hover:underline bg-transparent',
};

const sizes = {
  default: 'h-10 px-4 py-2 text-sm',
  sm: 'h-8 px-3 py-1 text-xs',
  lg: 'h-12 px-6 py-3 text-base',
  icon: 'h-9 w-9 p-0 flex items-center justify-center',
};

export const Button = forwardRef(
  ({ className, variant = 'default', size = 'default', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium',
          'transition-all duration-200 ease-out',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)] focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          'active:scale-[0.98]',
          'cursor-pointer',
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
