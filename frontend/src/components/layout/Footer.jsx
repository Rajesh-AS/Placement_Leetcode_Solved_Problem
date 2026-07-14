import { Link } from 'react-router-dom';
import { Building2, MapPin, GraduationCap, Phone, Mail, Heart } from 'lucide-react';

const AREAS = [
  'Peelamedu', 'Gandhipuram', 'RS Puram', 'Singanallur', 'Saravanampatti',
  'Ganapathy', 'Saibaba Colony', 'Kuniyamuthur', 'Kalapatti', 'Kovaipudur',
];

const COLLEGES = [
  'PSG Tech', 'Kumaraguru', 'Karunya', 'Rathinam', 'Sri Krishna',
  'CIT', 'SNS College', 'Amrita University',
];

export function Footer() {
  return (
    <footer className="bg-[var(--primary)] text-white mt-auto">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand */}
          <div className="lg:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center">
                <Building2 className="h-6 w-6 text-[var(--gold-light)]" />
              </div>
              <div>
                <h3 className="text-xl font-extrabold">StayFinder</h3>
                <p className="text-[10px] font-semibold tracking-wider text-[var(--gold-light)]">COIMBATORE</p>
              </div>
            </div>
            <p className="text-white/70 text-sm leading-relaxed mb-4">
              Find the perfect hostel, PG, or co-living space in Coimbatore.
              Safe stays, affordable rents, and trusted owners.
            </p>
            <div className="flex items-center gap-2 text-sm text-white/70">
              <Phone className="w-4 h-4" />
              <span>+91 422 2300 100</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-white/70 mt-1">
              <Mail className="w-4 h-4" />
              <span>hello@stayfinder.in</span>
            </div>
          </div>

          {/* Browse by Area */}
          <div>
            <h4 className="font-semibold text-[var(--gold-light)] mb-4 flex items-center gap-2">
              <MapPin className="w-4 h-4" /> Browse by Area
            </h4>
            <ul className="space-y-2 text-sm">
              {AREAS.map(area => (
                <li key={area}>
                  <Link
                    to={`/search?area=${encodeURIComponent(area)}`}
                    className="text-white/70 hover:text-white transition-colors hover:pl-1 inline-block transition-all duration-200"
                  >
                    {area}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Browse by College */}
          <div>
            <h4 className="font-semibold text-[var(--gold-light)] mb-4 flex items-center gap-2">
              <GraduationCap className="w-4 h-4" /> Near Colleges
            </h4>
            <ul className="space-y-2 text-sm">
              {COLLEGES.map(college => (
                <li key={college}>
                  <Link
                    to={`/search?college=${encodeURIComponent(college)}`}
                    className="text-white/70 hover:text-white transition-colors hover:pl-1 inline-block transition-all duration-200"
                  >
                    Near {college}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-[var(--gold-light)] mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/search?gender=boys" className="text-white/70 hover:text-white transition-colors">
                  Boys Hostels
                </Link>
              </li>
              <li>
                <Link to="/search?gender=girls" className="text-white/70 hover:text-white transition-colors">
                  Girls Hostels
                </Link>
              </li>
              <li>
                <Link to="/search?property_type=pg" className="text-white/70 hover:text-white transition-colors">
                  PG Accommodations
                </Link>
              </li>
              <li>
                <Link to="/search?property_type=coliving" className="text-white/70 hover:text-white transition-colors">
                  Co-Living Spaces
                </Link>
              </li>
              <li>
                <Link to="/register" className="text-white/70 hover:text-white transition-colors">
                  List Your Property
                </Link>
              </li>
              <li>
                <a href="#" className="text-white/70 hover:text-white transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="text-white/70 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-white/70 hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex flex-col md:flex-row justify-between items-center gap-2 text-sm text-white/60">
          <p>© {new Date().getFullYear()} StayFinder Coimbatore. All rights reserved.</p>
          <p className="flex items-center gap-1">
            Made in Coimbatore with <Heart className="w-3.5 h-3.5 text-red-400 fill-red-400" /> for students
          </p>
        </div>
      </div>
    </footer>
  );
}
