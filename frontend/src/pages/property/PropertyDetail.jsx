import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { propertyService } from '@/services/propertyService';
import { reviewService } from '@/services/reviewService';
import { Button } from '@/components/common/Button';
import { PropertyCard } from '@/components/common/PropertyCard';
import {
  MapPin, Star, Heart, Share2, Shield, Calendar, Bed, Check, Info,
  Phone, Mail, MessageSquare, ChevronLeft, ChevronRight, X, User,
  Utensils, Clock, CreditCard, Home, ArrowLeft
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export function PropertyDetail() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxIndex, setLightboxIndex] = useState(0);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [similar, setSimilar] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const propData = await propertyService.getPropertyById(id);
        setProperty(propData);

        // Fetch reviews
        try {
          const revData = await reviewService.getPropertyReviews(id);
          setReviews(revData.results || revData || []);
        } catch { /* reviews may not be available */ }

        // Fetch similar properties
        try {
          const simData = await propertyService.getProperties({
            area: propData.area,
            gender: propData.gender,
          });
          const simList = (simData.results || simData || []).filter(p => p.id !== propData.id).slice(0, 4);
          setSimilar(simList);
        } catch { /* similar may not be available */ }
      } catch (err) {
        console.error('Error fetching property details', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    alert('Link copied to clipboard!');
  };

  const allImages = property?.images?.length > 0
    ? property.images.map(img => img.image_url)
    : property?.cover_image
      ? [property.cover_image]
      : [];

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="shimmer h-[400px] rounded-2xl mb-8" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="shimmer h-8 w-2/3 rounded-lg" />
            <div className="shimmer h-4 w-1/2 rounded" />
            <div className="shimmer h-32 rounded-xl" />
          </div>
          <div className="shimmer h-64 rounded-2xl" />
        </div>
      </div>
    );
  }

  if (!property) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <h2 className="text-2xl font-bold">Property not found</h2>
        <Button variant="outline" onClick={() => navigate('/search')}>
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to search
        </Button>
      </div>
    );
  }

  return (
    <>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Back button */}
        <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] mb-4 cursor-pointer transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back
        </button>

        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-[var(--foreground)]">{property.name}</h1>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-[var(--muted-foreground)]">
              <span className="flex items-center gap-1 font-semibold text-[var(--foreground)]">
                <Star className="w-4 h-4 star-filled" />
                {property.avg_rating > 0 ? Number(property.avg_rating).toFixed(1) : 'New'}
                <span className="font-normal text-[var(--muted-foreground)]">
                  ({property.total_reviews || reviews.length} reviews)
                </span>
              </span>
              <span className="flex items-center gap-1">
                <MapPin className="w-4 h-4" /> {property.area}, {property.city}
              </span>
              {property.is_verified && (
                <span className="verified-badge">
                  <Shield className="w-3 h-3" /> Verified
                </span>
              )}
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={handleShare}>
              <Share2 className="w-4 h-4 mr-1.5" /> Share
            </Button>
            {user?.role === 'student' && (
              <Button variant="outline" size="sm">
                <Heart className="w-4 h-4 mr-1.5" /> Save
              </Button>
            )}
          </div>
        </div>

        {/* Image Gallery */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-2 h-[300px] sm:h-[400px] mb-10 rounded-2xl overflow-hidden">
          <div
            className="md:col-span-2 md:row-span-2 h-full bg-[var(--muted)] cursor-pointer relative group"
            onClick={() => { setLightboxIndex(0); setLightboxOpen(true); }}
          >
            {allImages[0] ? (
              <img src={allImages[0]} alt="Cover" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-[var(--secondary)]">
                <Home className="w-12 h-12 text-[var(--muted-foreground)]" />
              </div>
            )}
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors" />
          </div>
          {allImages.slice(1, 5).map((img, idx) => (
            <div
              key={idx}
              className="hidden md:block h-full bg-[var(--muted)] cursor-pointer relative group"
              onClick={() => { setLightboxIndex(idx + 1); setLightboxOpen(true); }}
            >
              <img src={img} alt={`View ${idx + 2}`} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors" />
              {idx === 3 && allImages.length > 5 && (
                <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <span className="text-white font-bold text-lg">+{allImages.length - 5} more</span>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-10">
            {/* About */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">About this property</h2>
              <p className="text-[var(--muted-foreground)] leading-relaxed whitespace-pre-line">{property.description}</p>
            </section>

            <hr className="border-[var(--border)]" />

            {/* Key Details */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">Key Details</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {[
                  { icon: Home, label: 'Type', value: property.property_type_display || property.property_type?.toUpperCase() },
                  { icon: User, label: 'For', value: property.gender_display || property.gender },
                  { icon: Bed, label: 'Available Beds', value: property.available_beds },
                  { icon: Utensils, label: 'Food', value: property.food_included ? `Yes (${property.food_type})` : 'Not Included' },
                  { icon: Clock, label: 'Notice Period', value: `${property.notice_period_days || 30} days` },
                  { icon: CreditCard, label: 'Deposit', value: `₹${Number(property.deposit).toLocaleString('en-IN')}` },
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-[var(--secondary)]">
                    <item.icon className="w-5 h-5 text-[var(--primary)] mt-0.5 shrink-0" />
                    <div>
                      <p className="text-xs text-[var(--muted-foreground)]">{item.label}</p>
                      <p className="text-sm font-semibold text-[var(--foreground)] capitalize">{item.value}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <hr className="border-[var(--border)]" />

            {/* Rooms */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">Available Rooms</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {property.rooms?.map(room => (
                  <div key={room.id} className="border border-[var(--border)] rounded-xl p-4 bg-[var(--card)] hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-bold capitalize flex items-center gap-2 text-[var(--foreground)]">
                        <Bed className="w-5 h-5 text-[var(--primary)]" /> {room.room_type} Room
                      </h3>
                      <span className="font-bold text-lg text-[var(--foreground)]">₹{Number(room.rent).toLocaleString('en-IN')}<span className="text-xs font-normal text-[var(--muted-foreground)]">/mo</span></span>
                    </div>
                    <div className="text-sm text-[var(--muted-foreground)] space-y-1.5">
                      <p className="flex items-center gap-1">
                        <span className={`w-2 h-2 rounded-full ${room.available_beds > 0 ? 'bg-green-500' : 'bg-red-500'}`} />
                        {room.available_beds > 0 ? `${room.available_beds} beds available` : 'No beds available'}
                        <span className="text-[var(--muted-foreground)]"> (of {room.total_beds})</span>
                      </p>
                      {room.has_attached_bathroom && (
                        <p className="text-green-600 flex items-center gap-1"><Check className="w-3 h-3" /> Attached Bathroom</p>
                      )}
                      {room.has_ac && (
                        <p className="text-green-600 flex items-center gap-1"><Check className="w-3 h-3" /> AC</p>
                      )}
                      {room.has_balcony && (
                        <p className="text-green-600 flex items-center gap-1"><Check className="w-3 h-3" /> Balcony</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <hr className="border-[var(--border)]" />

            {/* Amenities */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">What this place offers</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {property.amenities_list?.map((amenity, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-3 rounded-lg bg-[var(--secondary)] text-[var(--foreground)]">
                    <Check className="w-5 h-5 text-[var(--primary)] shrink-0" />
                    <span className="text-sm">{amenity}</span>
                  </div>
                ))}
              </div>
            </section>

            <hr className="border-[var(--border)]" />

            {/* House Rules */}
            {property.house_rules?.length > 0 && (
              <>
                <section>
                  <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">House Rules</h2>
                  <ul className="space-y-2">
                    {property.house_rules.map((rule, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-[var(--muted-foreground)]">
                        <span className="text-[var(--primary)] mt-1">•</span>
                        {rule}
                      </li>
                    ))}
                  </ul>
                </section>
                <hr className="border-[var(--border)]" />
              </>
            )}

            {/* Location */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">Location</h2>
              <p className="text-[var(--muted-foreground)] mb-4">{property.address}, {property.area}, {property.city} - {property.pincode}</p>

              {property.nearby_colleges?.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-semibold text-sm text-[var(--foreground)] mb-2">Nearby Colleges:</h4>
                  <div className="flex flex-wrap gap-2">
                    {property.nearby_colleges.map((college, idx) => (
                      <span key={idx} className="text-xs bg-[var(--secondary)] text-[var(--secondary-foreground)] px-3 py-1.5 rounded-full">
                        🎓 {college}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {property.nearby_bus_stops?.length > 0 && (
                <div>
                  <h4 className="font-semibold text-sm text-[var(--foreground)] mb-2">Nearby Bus Stops:</h4>
                  <div className="flex flex-wrap gap-2">
                    {property.nearby_bus_stops.map((stop, idx) => (
                      <span key={idx} className="text-xs bg-[var(--secondary)] text-[var(--secondary-foreground)] px-3 py-1.5 rounded-full">
                        🚌 {stop}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Map */}
              <div className="mt-6 h-[300px] w-full rounded-2xl overflow-hidden border border-[var(--border)] z-0 relative">
                <MapContainer 
                  center={[property.latitude || 11.0168, property.longitude || 76.9558]} 
                  zoom={14} 
                  scrollWheelZoom={false} 
                  className="h-full w-full z-0"
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  <Marker position={[property.latitude || 11.0168, property.longitude || 76.9558]}>
                    <Popup>
                      <strong>{property.name}</strong><br />
                      {property.area}, {property.city}
                    </Popup>
                  </Marker>
                </MapContainer>
              </div>
            </section>

            <hr className="border-[var(--border)]" />

            {/* Reviews */}
            <section>
              <h2 className="text-xl font-bold mb-4 text-[var(--foreground)]">
                Reviews {reviews.length > 0 && `(${reviews.length})`}
              </h2>
              {reviews.length > 0 ? (
                <div className="space-y-4">
                  {reviews.slice(0, 6).map((review, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-[var(--secondary)] border border-[var(--border)]">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="w-8 h-8 rounded-full bg-[var(--primary)]/10 flex items-center justify-center">
                          <User className="w-4 h-4 text-[var(--primary)]" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-[var(--foreground)]">
                            {review.user_name || review.user?.first_name || 'Student'}
                          </p>
                          <div className="flex items-center gap-1">
                            {Array.from({ length: 5 }).map((_, i) => (
                              <Star key={i} className={`w-3 h-3 ${i < review.rating ? 'star-filled' : 'text-[var(--border)]'}`} />
                            ))}
                          </div>
                        </div>
                      </div>
                      <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">{review.comment}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-[var(--muted-foreground)] text-sm">No reviews yet. Be the first to review!</p>
              )}
            </section>
          </div>

          {/* Sidebar - Booking Card */}
          <div className="relative">
            <div className="sticky top-24 glass-card rounded-2xl p-6 space-y-5">
              {/* Price */}
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-bold text-[var(--foreground)]">₹{Number(property.rent_min).toLocaleString('en-IN')}</span>
                <span className="text-[var(--muted-foreground)]">to</span>
                <span className="text-2xl font-bold text-[var(--foreground)]">₹{Number(property.rent_max).toLocaleString('en-IN')}</span>
                <span className="text-[var(--muted-foreground)]">/ month</span>
              </div>

              {/* Details */}
              <div className="space-y-3 border border-[var(--border)] rounded-xl p-4 text-sm">
                <div className="flex justify-between pb-2 border-b border-[var(--border)]">
                  <span className="font-medium text-[var(--muted-foreground)]">Deposit</span>
                  <span className="font-semibold text-[var(--foreground)]">₹{Number(property.deposit).toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between pb-2 border-b border-[var(--border)]">
                  <span className="font-medium text-[var(--muted-foreground)]">Food</span>
                  <span className="font-semibold text-[var(--foreground)]">{property.food_included ? `Yes (${property.food_type})` : 'Not Included'}</span>
                </div>
                <div className="flex justify-between pb-2 border-b border-[var(--border)]">
                  <span className="font-medium text-[var(--muted-foreground)]">Available</span>
                  <span className="font-semibold text-green-600">{property.available_beds} beds</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium text-[var(--muted-foreground)]">Notice Period</span>
                  <span className="font-semibold text-[var(--foreground)]">{property.notice_period_days || 30} days</span>
                </div>
              </div>

              {/* CTA Buttons */}
              {!user ? (
                <Button className="w-full" size="lg" onClick={() => navigate('/login')}>
                  Log in to Book Visit
                </Button>
              ) : user.role === 'student' ? (
                <Button className="w-full" size="lg" onClick={() => setShowBookingModal(true)}>
                  <Calendar className="mr-2 h-4 w-4" /> Schedule a Visit
                </Button>
              ) : (
                <div className="p-3 rounded-lg bg-[var(--secondary)] text-sm text-center flex items-center justify-center gap-2 text-[var(--muted-foreground)]">
                  <Info className="w-4 h-4 text-[var(--primary)]" /> Logged in as {user.role}
                </div>
              )}

              {/* Contact */}
              <div className="space-y-2 pt-2">
                {property.contact_phone && (
                  <a href={`tel:${property.contact_phone}`} className="flex items-center gap-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--primary)] transition-colors">
                    <Phone className="w-4 h-4" /> {property.contact_phone}
                  </a>
                )}
                {property.contact_email && (
                  <a href={`mailto:${property.contact_email}`} className="flex items-center gap-2 text-sm text-[var(--muted-foreground)] hover:text-[var(--primary)] transition-colors">
                    <Mail className="w-4 h-4" /> {property.contact_email}
                  </a>
                )}
                {user && (
                  <Button variant="outline" className="w-full mt-2">
                    <MessageSquare className="w-4 h-4 mr-2" /> Message Owner
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Similar Properties */}
        {similar.length > 0 && (
          <section className="mt-16 mb-8">
            <h2 className="text-xl font-bold mb-6 text-[var(--foreground)]">
              Similar Properties in <span className="text-[var(--primary)]">{property.area}</span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              {similar.map(p => <PropertyCard key={p.id} property={p} />)}
            </div>
          </section>
        )}
      </div>

      {/* Lightbox */}
      {lightboxOpen && allImages.length > 0 && (
        <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center animate-fade-in">
          <button onClick={() => setLightboxOpen(false)} className="absolute top-4 right-4 p-2 text-white/80 hover:text-white cursor-pointer">
            <X className="w-8 h-8" />
          </button>
          <button
            onClick={() => setLightboxIndex((lightboxIndex - 1 + allImages.length) % allImages.length)}
            className="absolute left-4 p-2 text-white/80 hover:text-white cursor-pointer"
          >
            <ChevronLeft className="w-8 h-8" />
          </button>
          <img
            src={allImages[lightboxIndex]}
            alt={`Image ${lightboxIndex + 1}`}
            className="max-h-[85vh] max-w-[90vw] object-contain rounded-lg"
          />
          <button
            onClick={() => setLightboxIndex((lightboxIndex + 1) % allImages.length)}
            className="absolute right-4 p-2 text-white/80 hover:text-white cursor-pointer"
          >
            <ChevronRight className="w-8 h-8" />
          </button>
          <div className="absolute bottom-4 text-white/60 text-sm">
            {lightboxIndex + 1} / {allImages.length}
          </div>
        </div>
      )}

      {/* Booking Modal */}
      {showBookingModal && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-[var(--card)] rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-[var(--foreground)]">Schedule a Visit</h3>
              <button onClick={() => setShowBookingModal(false)} className="p-1 hover:bg-[var(--secondary)] rounded-lg cursor-pointer">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={(e) => { e.preventDefault(); alert('Visit request submitted! The owner will confirm.'); setShowBookingModal(false); }}>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Preferred Date</label>
                  <input
                    type="date"
                    required
                    className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)]"
                    min={new Date().toISOString().split('T')[0]}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Preferred Time</label>
                  <select className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)]">
                    <option>10:00 AM - 12:00 PM</option>
                    <option>12:00 PM - 2:00 PM</option>
                    <option>2:00 PM - 4:00 PM</option>
                    <option>4:00 PM - 6:00 PM</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Room Preference</label>
                  <select className="w-full h-10 rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)]">
                    <option>Any Room</option>
                    {property.rooms?.map(r => (
                      <option key={r.id} value={r.room_type}>{r.room_type} - ₹{r.rent}/mo</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-[var(--foreground)] mb-1.5 block">Message (optional)</label>
                  <textarea
                    rows={3}
                    className="w-full rounded-lg border border-[var(--input)] bg-[var(--card)] px-3 py-2 text-sm text-[var(--foreground)] resize-none"
                    placeholder="Any questions for the owner?"
                  />
                </div>
              </div>
              <Button type="submit" className="w-full mt-5">Confirm Visit Request</Button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
