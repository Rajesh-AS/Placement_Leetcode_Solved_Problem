import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { propertyService } from '@/services/propertyService';
import { PropertyCard } from '@/components/common/PropertyCard';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import {
  Search, Filter, MapPin, SlidersHorizontal, X, ChevronDown,
  ArrowUpDown, Sparkles
} from 'lucide-react';

const AREAS = [
  'Peelamedu', 'Gandhipuram', 'RS Puram', 'Singanallur', 'Saravanampatti',
  'Ganapathy', 'Saibaba Colony', 'Kuniyamuthur', 'Kalapatti', 'Kovaipudur',
  'Sulur', 'Podanur', 'Sundarapuram', 'Perur', 'Ukkadam',
  'Hope College', 'Mettupalayam', 'Pollachi', 'Madukkarai', 'Kinathukadavu',
];

const COLLEGES = [
  'PSG Tech', 'PSG College', 'Kumaraguru College', 'Karunya University',
  'Rathinam College', 'Sri Krishna College', 'SNS College', 'NGP College',
  'Hindusthan College', 'CIT', 'Government Arts College', 'Amrita University',
];

export function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [parsedFilters, setParsedFilters] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const [searchInput, setSearchInput] = useState(searchParams.get('q') || '');

  const query = searchParams.get('q') || '';

  const [filters, setFilters] = useState({
    area: searchParams.get('area') || '',
    college: searchParams.get('college') || '',
    property_type: searchParams.get('property_type') || '',
    gender: searchParams.get('gender') || '',
    max_rent: searchParams.get('max_rent') || '',
    min_rent: searchParams.get('min_rent') || '',
    food_included: searchParams.get('food_included') || '',
    is_verified: searchParams.get('is_verified') || '',
    ordering: searchParams.get('ordering') || '',
  });

  useEffect(() => {
    fetchProperties();
  }, [searchParams]);

  const fetchProperties = async () => {
    setLoading(true);
    try {
      if (query) {
        const res = await propertyService.smartSearch(query);
        setProperties(res.results || []);
        setParsedFilters(res.parsed_filters || null);
      } else {
        const params = {};
        searchParams.forEach((value, key) => {
          if (key !== 'q') params[key] = value;
        });
        // Map 'area' to backend field
        if (params.area) { params.area = params.area; }
        if (params.college) {
          // Backend uses 'college' filter on nearby_colleges
          params.college = params.college;
        }
        const res = await propertyService.getProperties(params);
        setProperties(res.results || res || []);
        setParsedFilters(null);
      }
    } catch (err) {
      console.error('Failed to fetch properties', err);
      setProperties([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchInput.trim()) params.set('q', searchInput.trim());
    setSearchParams(params);
  };

  const handleFilterApply = () => {
    const newParams = new URLSearchParams();
    if (query) newParams.set('q', query);
    Object.entries(filters).forEach(([key, value]) => {
      if (value) newParams.set(key, value);
    });
    setSearchParams(newParams);
    setShowFilters(false);
  };

  const handleClearFilters = () => {
    setFilters({
      area: '', college: '', property_type: '', gender: '',
      max_rent: '', min_rent: '', food_included: '', is_verified: '', ordering: '',
    });
    setSearchInput('');
    setSearchParams({});
  };

  const activeFilterCount = Object.values(filters).filter(Boolean).length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Search Bar */}
      <div className="mb-6">
        <form onSubmit={handleSearch} className="flex gap-2 max-w-2xl">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[var(--muted-foreground)]" />
            <input
              type="text"
              placeholder='Try "girls PG near Kumaraguru under 6000 with food"'
              className="w-full h-11 rounded-xl border border-[var(--border)] bg-[var(--card)] pl-10 pr-4 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/30 focus:border-[var(--primary)] transition-all"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
          </div>
          <Button type="submit" className="h-11 px-5 rounded-xl shrink-0">
            Search
          </Button>
        </form>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Filters Sidebar */}
        <aside className={`w-full lg:w-72 shrink-0 ${showFilters ? 'block' : 'hidden lg:block'}`}>
          <div className="glass-card rounded-2xl p-5 sticky top-24 space-y-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 font-semibold text-[var(--foreground)]">
                <SlidersHorizontal className="w-5 h-5 text-[var(--primary)]" />
                Filters
                {activeFilterCount > 0 && (
                  <span className="bg-[var(--primary)] text-white text-xs px-2 py-0.5 rounded-full">
                    {activeFilterCount}
                  </span>
                )}
              </div>
              {activeFilterCount > 0 && (
                <button onClick={handleClearFilters} className="text-xs text-[var(--primary)] hover:underline cursor-pointer">
                  Clear all
                </button>
              )}
            </div>

            {/* Area */}
            <div>
              <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Area</label>
              <div className="relative">
                <select
                  className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                  value={filters.area}
                  onChange={e => setFilters({ ...filters, area: e.target.value })}
                >
                  <option value="">All Areas</option>
                  {AREAS.map(a => <option key={a} value={a}>{a}</option>)}
                </select>
                <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
              </div>
            </div>

            {/* College */}
            <div>
              <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Near College</label>
              <div className="relative">
                <select
                  className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                  value={filters.college}
                  onChange={e => setFilters({ ...filters, college: e.target.value })}
                >
                  <option value="">Any College</option>
                  {COLLEGES.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
                <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
              </div>
            </div>

            {/* Budget */}
            <div>
              <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Budget (₹/month)</label>
              <div className="flex gap-2">
                <Input
                  type="number"
                  placeholder="Min"
                  value={filters.min_rent}
                  onChange={e => setFilters({ ...filters, min_rent: e.target.value })}
                />
                <Input
                  type="number"
                  placeholder="Max"
                  value={filters.max_rent}
                  onChange={e => setFilters({ ...filters, max_rent: e.target.value })}
                />
              </div>
            </div>

            {/* Property Type */}
            <div>
              <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Type</label>
              <div className="relative">
                <select
                  className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                  value={filters.property_type}
                  onChange={e => setFilters({ ...filters, property_type: e.target.value })}
                >
                  <option value="">All Types</option>
                  <option value="pg">Paying Guest (PG)</option>
                  <option value="hostel">Hostel</option>
                  <option value="coliving">Co-Living</option>
                  <option value="flat">Flat / Apartment</option>
                </select>
                <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
              </div>
            </div>

            {/* Gender */}
            <div>
              <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">For</label>
              <div className="relative">
                <select
                  className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                  value={filters.gender}
                  onChange={e => setFilters({ ...filters, gender: e.target.value })}
                >
                  <option value="">Anyone</option>
                  <option value="boys">Boys</option>
                  <option value="girls">Girls</option>
                  <option value="coliving">Co-Living (Both)</option>
                </select>
                <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
              </div>
            </div>

            {/* Food */}
            <div>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.food_included === 'true'}
                  onChange={e => setFilters({ ...filters, food_included: e.target.checked ? 'true' : '' })}
                  className="w-4 h-4 rounded border-[var(--border)] text-[var(--primary)] focus:ring-[var(--primary)]"
                />
                <span className="text-sm text-[var(--foreground)]">Food Included</span>
              </label>
            </div>

            {/* Verified Only */}
            <div>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.is_verified === 'true'}
                  onChange={e => setFilters({ ...filters, is_verified: e.target.checked ? 'true' : '' })}
                  className="w-4 h-4 rounded border-[var(--border)] text-[var(--primary)] focus:ring-[var(--primary)]"
                />
                <span className="text-sm text-[var(--foreground)]">Verified Only</span>
              </label>
            </div>

            <Button className="w-full" onClick={handleFilterApply}>
              Apply Filters
            </Button>
          </div>
        </aside>

        {/* Results */}
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-[var(--foreground)]">
                {query ? `Results for "${query}"` : 'Explore Properties'}
              </h1>
              <p className="text-sm text-[var(--muted-foreground)] mt-0.5">
                {loading ? 'Searching...' : `Found ${properties.length} properties in Coimbatore`}
              </p>
            </div>

            <div className="flex items-center gap-2">
              {/* Mobile filter toggle */}
              <Button
                variant="outline"
                size="sm"
                className="lg:hidden"
                onClick={() => setShowFilters(!showFilters)}
              >
                <Filter className="w-4 h-4 mr-1" />
                Filters
                {activeFilterCount > 0 && (
                  <span className="ml-1 bg-[var(--primary)] text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                    {activeFilterCount}
                  </span>
                )}
              </Button>

              {/* Sort */}
              <div className="relative">
                <select
                  className="h-9 rounded-lg border border-[var(--border)] bg-[var(--card)] pl-8 pr-3 text-xs text-[var(--foreground)] appearance-none cursor-pointer"
                  value={filters.ordering}
                  onChange={e => {
                    const newFilters = { ...filters, ordering: e.target.value };
                    setFilters(newFilters);
                    const params = new URLSearchParams(searchParams);
                    if (e.target.value) params.set('ordering', e.target.value);
                    else params.delete('ordering');
                    setSearchParams(params);
                  }}
                >
                  <option value="">Relevance</option>
                  <option value="rent_min">Price: Low to High</option>
                  <option value="-rent_min">Price: High to Low</option>
                  <option value="-avg_rating">Highest Rated</option>
                  <option value="-created_at">Newest First</option>
                </select>
                <ArrowUpDown className="absolute left-2.5 top-2.5 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
              </div>
            </div>
          </div>

          {/* AI Parsed Filters */}
          {parsedFilters && Object.keys(parsedFilters).length > 0 && (
            <div className="mb-4 p-3 rounded-xl bg-[var(--primary)]/5 border border-[var(--primary)]/20 flex flex-wrap items-center gap-2">
              <Sparkles className="w-4 h-4 text-[var(--primary)] shrink-0" />
              <span className="text-sm text-[var(--muted-foreground)] mr-1">Smart filters:</span>
              {Object.entries(parsedFilters).map(([k, v]) => (
                <span
                  key={k}
                  className="bg-[var(--primary)]/10 text-[var(--primary)] px-2.5 py-1 rounded-full text-xs font-medium capitalize"
                >
                  {k.replace('_', ' ')}: {Array.isArray(v) ? v.join(', ') : v.toString()}
                </span>
              ))}
            </div>
          )}

          {/* Results Grid */}
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="shimmer rounded-2xl h-[360px]" />
              ))}
            </div>
          ) : properties.length === 0 ? (
            <div className="text-center py-20 rounded-2xl border border-[var(--border)] bg-[var(--card)]">
              <div className="w-16 h-16 rounded-full bg-[var(--secondary)] flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-[var(--muted-foreground)]" />
              </div>
              <h3 className="text-xl font-semibold text-[var(--foreground)] mb-2">No properties found</h3>
              <p className="text-[var(--muted-foreground)] mb-4">Try adjusting your filters or search query.</p>
              <Button variant="outline" onClick={handleClearFilters}>Clear all filters</Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
              {properties.map(property => (
                <PropertyCard key={property.id} property={property} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
