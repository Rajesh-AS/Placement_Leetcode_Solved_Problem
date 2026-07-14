import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import { PropertyCard } from '@/components/common/PropertyCard';
import { propertyService } from '@/services/propertyService';
import {
  Search, MapPin, Building2, ShieldCheck, Star, Sparkles,
  GraduationCap, Users, ArrowRight, CheckCircle2, ChevronDown
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

export function HomePage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedArea, setSelectedArea] = useState('');
  const [selectedGender, setSelectedGender] = useState('');
  const [featured, setFeatured] = useState([]);
  const [popular, setPopular] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [featuredRes, popularRes] = await Promise.allSettled([
          propertyService.getFeatured(),
          propertyService.getPopular(),
        ]);
        if (featuredRes.status === 'fulfilled') setFeatured(featuredRes.value?.results || featuredRes.value || []);
        if (popularRes.status === 'fulfilled') setPopular(popularRes.value?.results || popularRes.value || []);
      } catch (err) {
        console.error('Error fetching homepage data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (searchQuery.trim()) params.set('q', searchQuery);
    if (selectedArea) params.set('area', selectedArea);
    if (selectedGender) params.set('gender', selectedGender);
    navigate(`/search?${params.toString()}`);
  };

  const handleAreaClick = (area) => {
    navigate(`/search?area=${encodeURIComponent(area)}`);
  };

  const handleCollegeClick = (college) => {
    navigate(`/search?college=${encodeURIComponent(college)}`);
  };

  return (
    <div className="flex flex-col">
      {/* ============================================================
          HERO SECTION
          ============================================================ */}
      <section className="relative min-h-[600px] lg:min-h-[650px] flex items-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <img
            src="https://images.unsplash.com/photo-1555854877-bab0e564b8d5?q=80&w=2069&auto=format&fit=crop"
            alt="Coimbatore cityscape"
            className="w-full h-full object-cover"
          />
          <div className="hero-gradient absolute inset-0" />
        </div>

        {/* Floating decorative elements */}
        <div className="absolute top-20 right-10 w-64 h-64 bg-[var(--gold)]/10 rounded-full blur-3xl animate-float hidden lg:block" />
        <div className="absolute bottom-20 left-10 w-48 h-48 bg-[var(--primary-light)]/10 rounded-full blur-3xl hidden lg:block" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 w-full">
          <div className="max-w-3xl">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-6 animate-fade-in-up">
              <Sparkles className="w-4 h-4 text-[var(--gold-light)]" />
              <span className="text-sm font-medium text-white/90">#1 Hostel Finder in Coimbatore</span>
            </div>

            {/* Heading */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white leading-tight mb-4 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              Find the Best{' '}
              <span className="text-gold-gradient">Hostel</span>
              <br />in Coimbatore
            </h1>

            {/* Tagline */}
            <p className="text-lg sm:text-xl text-white/80 mb-8 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              Safe Stay • Affordable Rent • Trusted Owners
            </p>

            {/* Search Widget */}
            <div className="glass-card rounded-2xl p-2 sm:p-3 max-w-2xl animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              <form onSubmit={handleSearch}>
                {/* Main search input */}
                <div className="flex items-center gap-2 px-3 py-2 mb-2">
                  <Search className="w-5 h-5 text-[var(--muted-foreground)] shrink-0" />
                  <input
                    type="text"
                    placeholder='Try "girls hostel near PSG under 5000 with wifi"'
                    className="w-full bg-transparent border-none focus:outline-none text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] text-sm sm:text-base"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>

                {/* Filter row */}
                <div className="flex flex-col sm:flex-row gap-2">
                  <div className="flex-1 relative">
                    <select
                      className="w-full h-10 rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                      value={selectedArea}
                      onChange={(e) => setSelectedArea(e.target.value)}
                    >
                      <option value="">All Areas</option>
                      {AREAS.map(a => <option key={a} value={a}>{a}</option>)}
                    </select>
                    <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
                  </div>

                  <div className="flex-1 relative">
                    <select
                      className="w-full h-10 rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] appearance-none cursor-pointer"
                      value={selectedGender}
                      onChange={(e) => setSelectedGender(e.target.value)}
                    >
                      <option value="">Boys & Girls</option>
                      <option value="boys">Boys Only</option>
                      <option value="girls">Girls Only</option>
                      <option value="coliving">Co-Living</option>
                    </select>
                    <ChevronDown className="absolute right-3 top-3 w-4 h-4 text-[var(--muted-foreground)] pointer-events-none" />
                  </div>

                  <Button type="submit" size="lg" className="h-10 px-6 rounded-lg shrink-0">
                    <Search className="w-4 h-4 mr-2" /> Search
                  </Button>
                </div>
              </form>
            </div>

            {/* Quick stats */}
            <div className="flex flex-wrap gap-6 mt-8 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              {[
                { icon: Building2, label: '500+ Stays', value: 'Listed' },
                { icon: GraduationCap, label: '12 Colleges', value: 'Covered' },
                { icon: MapPin, label: '20+ Areas', value: 'in Coimbatore' },
              ].map((stat, i) => (
                <div key={i} className="flex items-center gap-2 text-white/80">
                  <stat.icon className="w-5 h-5 text-[var(--gold-light)]" />
                  <span className="text-sm font-medium">{stat.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ============================================================
          FEATURED PROPERTIES
          ============================================================ */}
      {featured.length > 0 && (
        <section className="py-16 bg-[var(--background)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-end mb-8">
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
                  Featured <span className="text-[var(--primary)]">Properties</span>
                </h2>
                <p className="text-[var(--muted-foreground)] mt-1">Hand-picked stays trusted by our community</p>
              </div>
              <Link to="/search?is_featured=true" className="hidden sm:flex items-center gap-1 text-[var(--primary)] font-semibold text-sm hover:underline">
                View all <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {featured.slice(0, 8).map(prop => (
                <PropertyCard key={prop.id} property={prop} />
              ))}
            </div>

            <div className="mt-6 text-center sm:hidden">
              <Link to="/search?is_featured=true">
                <Button variant="outline">View all featured →</Button>
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* ============================================================
          BROWSE BY AREA
          ============================================================ */}
      <section className="py-16 bg-[var(--secondary)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
              Browse by <span className="text-[var(--primary)]">Area</span>
            </h2>
            <p className="text-[var(--muted-foreground)] mt-2">Explore hostels and PGs across Coimbatore</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {AREAS.map((area) => (
              <button
                key={area}
                onClick={() => handleAreaClick(area)}
                className="group flex items-center gap-2 px-4 py-3 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-[var(--primary)] hover:shadow-md transition-all text-left cursor-pointer"
              >
                <MapPin className="w-4 h-4 text-[var(--primary)] shrink-0 group-hover:scale-110 transition-transform" />
                <span className="text-sm font-medium text-[var(--foreground)] truncate">{area}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================
          BROWSE BY COLLEGE
          ============================================================ */}
      <section className="py-16 bg-[var(--background)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
              Near Your <span className="text-[var(--gold)]">College</span>
            </h2>
            <p className="text-[var(--muted-foreground)] mt-2">Find stays walking distance from campus</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {COLLEGES.map((college) => (
              <button
                key={college}
                onClick={() => handleCollegeClick(college)}
                className="group flex items-center gap-3 px-4 py-4 rounded-xl bg-[var(--card)] border border-[var(--border)] hover:border-[var(--gold)] hover:shadow-md transition-all text-left cursor-pointer"
              >
                <div className="w-10 h-10 rounded-lg bg-[var(--gold)]/10 flex items-center justify-center shrink-0 group-hover:bg-[var(--gold)]/20 transition-colors">
                  <GraduationCap className="w-5 h-5 text-[var(--gold)]" />
                </div>
                <span className="text-sm font-medium text-[var(--foreground)]">{college}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================
          HOW IT WORKS
          ============================================================ */}
      <section className="py-16 bg-[var(--secondary)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
              How It <span className="text-[var(--primary)]">Works</span>
            </h2>
            <p className="text-[var(--muted-foreground)] mt-2">Finding your ideal stay is just 3 steps away</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                icon: Search,
                title: 'Search & Filter',
                desc: 'Search by area, college, budget, or just describe what you need in natural language.',
              },
              {
                step: '02',
                icon: Building2,
                title: 'Compare & Choose',
                desc: 'View verified listings with photos, amenities, rooms, and genuine student reviews.',
              },
              {
                step: '03',
                icon: CheckCircle2,
                title: 'Book a Visit',
                desc: 'Schedule a visit, chat with the owner, and secure your perfect stay.',
              },
            ].map((item, i) => (
              <div key={i} className="relative flex flex-col items-center text-center p-8 rounded-2xl bg-[var(--card)] border border-[var(--border)] hover:shadow-lg transition-shadow group">
                <span className="absolute -top-4 left-6 text-5xl font-black text-[var(--primary)]/10 group-hover:text-[var(--primary)]/20 transition-colors">
                  {item.step}
                </span>
                <div className="w-14 h-14 rounded-2xl bg-[var(--primary)]/10 flex items-center justify-center mb-5 group-hover:bg-[var(--primary)]/20 transition-colors">
                  <item.icon className="w-7 h-7 text-[var(--primary)]" />
                </div>
                <h3 className="text-lg font-bold mb-2 text-[var(--foreground)]">{item.title}</h3>
                <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================
          WHY CHOOSE US
          ============================================================ */}
      <section className="py-16 bg-[var(--background)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
              Why Students <span className="text-[var(--primary)]">Trust Us</span>
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: ShieldCheck, title: 'Verified Listings', desc: 'Every property is verified by our team for safety and quality.' },
              { icon: Sparkles, title: 'Smart Search', desc: 'Just type what you need. Our AI understands natural language queries.' },
              { icon: Star, title: 'Genuine Reviews', desc: 'Real reviews from real students who stayed at these properties.' },
              { icon: Users, title: 'Direct Owner Contact', desc: 'Chat directly with property owners. No brokers, no extra fees.' },
            ].map((item, i) => (
              <div key={i} className="p-6 rounded-2xl border border-[var(--border)] bg-[var(--card)] hover:shadow-md transition-shadow text-center group">
                <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center mx-auto mb-4 group-hover:bg-[var(--primary)]/20 transition-colors">
                  <item.icon className="w-6 h-6 text-[var(--primary)]" />
                </div>
                <h3 className="font-bold text-[var(--foreground)] mb-2">{item.title}</h3>
                <p className="text-sm text-[var(--muted-foreground)]">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================
          POPULAR PROPERTIES
          ============================================================ */}
      {popular.length > 0 && (
        <section className="py-16 bg-[var(--secondary)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-end mb-8">
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">
                  Popular <span className="text-[var(--primary)]">Stays</span>
                </h2>
                <p className="text-[var(--muted-foreground)] mt-1">Top-rated properties loved by students</p>
              </div>
              <Link to="/search?ordering=-avg_rating" className="hidden sm:flex items-center gap-1 text-[var(--primary)] font-semibold text-sm hover:underline">
                View all <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {popular.slice(0, 8).map(prop => (
                <PropertyCard key={prop.id} property={prop} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ============================================================
          CTA SECTION
          ============================================================ */}
      <section className="py-20 bg-[var(--primary)] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/3" />
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-[var(--gold)]/10 rounded-full translate-y-1/2 -translate-x-1/3" />

        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white mb-4">
            Own a Hostel or PG in Coimbatore?
          </h2>
          <p className="text-lg text-white/80 mb-8 max-w-2xl mx-auto">
            List your property for free and reach thousands of students looking for accommodation near their college.
          </p>
          <Link to="/register">
            <Button variant="gold" size="lg" className="text-base px-8">
              List Your Property Free →
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
