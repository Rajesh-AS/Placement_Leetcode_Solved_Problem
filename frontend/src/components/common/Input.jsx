import { forwardRef } from 'react';
import { clsx } from 'clsx';

export const Input = forwardRef(
  ({ className, error, type = 'text', ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          type={type}
          ref={ref}
          className={clsx(
            'flex h-10 w-full rounded-lg border bg-[var(--card)] px-3 py-2 text-sm',
            'text-[var(--foreground)] placeholder:text-[var(--muted-foreground)]',
            'transition-all duration-200',
            'focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/30 focus:border-[var(--primary)]',
            'disabled:cursor-not-allowed disabled:opacity-50',
            error
              ? 'border-[var(--destructive)] focus:ring-[var(--destructive)]/30 focus:border-[var(--destructive)]'
              : 'border-[var(--input)]',
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-1 text-xs text-[var(--destructive)]">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
