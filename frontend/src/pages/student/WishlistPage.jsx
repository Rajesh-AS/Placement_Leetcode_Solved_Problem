import { useState, useEffect } from 'react';
import { wishlistService } from '@/services/wishlistService';
import { PropertyCard } from '@/components/common/PropertyCard';
import { Button } from '@/components/common/Button';
import { Heart, Search, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function WishlistPage() {
  const [wishlists, setWishlists] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchWishlists();
  }, []);

  const fetchWishlists = async () => {
    try {
      const res = await wishlistService.getWishlists();
      setWishlists(res.results || res || []);
    } catch (err) {
      console.error('Failed to fetch wishlists', err);
    } finally {
      setLoading(false);
    }
  };

  const handleWishlistChange = () => {
    fetchWishlists();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] mb-6 cursor-pointer transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center">
          <Heart className="w-6 h-6 text-red-500 fill-red-500" />
        </div>
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">Your Wishlists</h1>
          <p className="text-sm text-[var(--muted-foreground)] mt-1">
            {loading ? 'Loading...' : `You have saved ${wishlists.length} properties`}
          </p>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="shimmer h-[360px] rounded-2xl" />
          ))}
        </div>
      ) : wishlists.length === 0 ? (
        <div className="text-center py-24 rounded-2xl border border-[var(--border)] bg-[var(--card)] mt-8">
          <div className="w-16 h-16 rounded-full bg-[var(--secondary)] flex items-center justify-center mx-auto mb-4">
            <Heart className="w-8 h-8 text-[var(--muted-foreground)]" />
          </div>
          <h3 className="text-xl font-semibold text-[var(--foreground)] mb-2">No saved properties yet</h3>
          <p className="text-[var(--muted-foreground)] mb-6 max-w-sm mx-auto">
            Explore hostels and PGs in Coimbatore and tap the heart icon to save your favorites here.
          </p>
          <Button onClick={() => navigate('/search')}>
            <Search className="w-4 h-4 mr-2" /> Start exploring
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {wishlists.map(item => (
            <PropertyCard 
              key={item.id} 
              property={item.property} 
              onWishlistChange={handleWishlistChange}
            />
          ))}
        </div>
      )}
    </div>
  );
}
