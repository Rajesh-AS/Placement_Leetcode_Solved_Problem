import { Link } from 'react-router-dom';
import { MapPin, Star, Heart, Shield, Wifi, UtensilsCrossed, Zap } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { wishlistService } from '@/services/wishlistService';

const AMENITY_ICONS = {
  'wifi': Wifi,
  'food included': UtensilsCrossed,
  'food': UtensilsCrossed,
  'power backup': Zap,
};

export function PropertyCard({ property, onWishlistChange }) {
  const { user } = useAuth();
  const [wishlisted, setWishlisted] = useState(false);
  const [imgError, setImgError] = useState(false);

  const handleWishlist = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) return;
    try {
      await wishlistService.addToWishlist(property.id);
      setWishlisted(!wishlisted);
      onWishlistChange?.();
    } catch (err) {
      console.error('Wishlist error', err);
    }
  };

  const coverImage = property.primary_image || property.cover_image;

  return (
    <Link
      to={`/property/${property.id}`}
      className="group property-card flex flex-col bg-[var(--card)] rounded-2xl border border-[var(--border)] overflow-hidden"
    >
      {/* Image */}
      <div className="relative h-52 bg-[var(--muted)] overflow-hidden">
        {coverImage && !imgError ? (
          <img
            src={coverImage}
            alt={property.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-[var(--secondary)]">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-2 rounded-full bg-[var(--primary)]/10 flex items-center justify-center">
                <MapPin className="w-8 h-8 text-[var(--primary)]" />
              </div>
              <span className="text-sm text-[var(--muted-foreground)]">{property.area}</span>
            </div>
          </div>
        )}

        {/* Type & Gender Badge */}
        <div className="absolute top-3 left-3 flex gap-1.5">
          <span className="glass px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wide text-[var(--foreground)]">
            {property.property_type_display || property.property_type}
          </span>
          <span className="glass px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wide text-[var(--foreground)]">
            {property.gender_display || property.gender}
          </span>
        </div>

        {/* Verified Badge */}
        {property.is_verified && (
          <div className="absolute bottom-3 left-3">
            <span className="verified-badge text-xs">
              <Shield className="w-3 h-3" /> Verified
            </span>
          </div>
        )}

        {/* Wishlist Button */}
        {user?.role === 'student' && (
          <button
            className="absolute top-3 right-3 p-2 glass rounded-full hover:scale-110 transition-transform"
            onClick={handleWishlist}
            title={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
          >
            <Heart
              className={`w-5 h-5 transition-colors ${
                wishlisted ? 'fill-red-500 text-red-500' : 'text-[var(--foreground)]'
              }`}
            />
          </button>
        )}

        {/* Featured Badge */}
        {property.is_featured && (
          <div className="absolute top-3 right-3">
            <span className="bg-[var(--gold)] text-[var(--accent-foreground)] px-2.5 py-1 rounded-full text-xs font-bold">
              ★ Featured
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        {/* Title & Rating */}
        <div className="flex justify-between items-start mb-1.5">
          <h3 className="font-bold text-[var(--foreground)] text-base line-clamp-1 group-hover:text-[var(--primary)] transition-colors">
            {property.name}
          </h3>
          <div className="flex items-center gap-1 text-sm font-semibold shrink-0 ml-2">
            <Star className="w-4 h-4 star-filled" />
            <span className="text-[var(--foreground)]">
              {property.avg_rating > 0 ? Number(property.avg_rating).toFixed(1) : 'New'}
            </span>
          </div>
        </div>

        {/* Location */}
        <div className="flex items-center text-sm text-[var(--muted-foreground)] mb-3">
          <MapPin className="w-3.5 h-3.5 mr-1 shrink-0" />
          <span className="line-clamp-1">{property.area}, {property.city}</span>
        </div>

        {/* Amenities */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {property.amenities_list?.slice(0, 4).map((amenity, idx) => {
            const IconComp = AMENITY_ICONS[amenity.toLowerCase()];
            return (
              <span
                key={idx}
                className="flex items-center gap-1 text-xs bg-[var(--secondary)] text-[var(--secondary-foreground)] px-2 py-1 rounded-md"
              >
                {IconComp && <IconComp className="w-3 h-3" />}
                <span className="truncate max-w-[70px]">{amenity}</span>
              </span>
            );
          })}
          {property.amenities_list?.length > 4 && (
            <span className="text-xs bg-[var(--secondary)] text-[var(--muted-foreground)] px-2 py-1 rounded-md">
              +{property.amenities_list.length - 4}
            </span>
          )}
        </div>

        {/* Price */}
        <div className="mt-auto pt-3 border-t border-[var(--border)] flex justify-between items-end">
          <div>
            <p className="text-xs text-[var(--muted-foreground)]">Starts from</p>
            <p className="font-bold text-lg text-[var(--foreground)]">
              ₹{Number(property.rent_min).toLocaleString('en-IN')}
              <span className="text-sm font-normal text-[var(--muted-foreground)]">/mo</span>
            </p>
          </div>
          <span className="text-xs text-[var(--primary)] font-semibold group-hover:underline">
            View Details →
          </span>
        </div>
      </div>
    </Link>
  );
}
