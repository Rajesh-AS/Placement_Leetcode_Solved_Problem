import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { Button } from '@/components/common/Button';
import { Building, Users, TrendingUp, Calendar, MapPin, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';

export function OwnerDashboard() {
  const [stats, setStats] = useState(null);
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch properties owned by this user
        const propsRes = await api.get('/properties/my/');
        setProperties(propsRes.data);
        
        // Mock stats for now until backend analytics endpoint is ready
        setStats({
          totalProperties: propsRes.data.length,
          totalViews: propsRes.data.reduce((sum, p) => sum + p.total_views, 0),
          activeVisits: 5,
          totalRevenue: '₹45,000'
        });
      } catch (err) {
        console.error('Failed to fetch dashboard data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) return <div className="p-8 text-center">Loading dashboard...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Owner Dashboard</h1>
        <Link to="/owner/properties/new">
          <Button><Plus className="w-4 h-4 mr-2" /> Add Property</Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-card p-6 rounded-xl border shadow-sm flex items-center gap-4">
          <div className="p-3 bg-primary/10 text-primary rounded-lg"><Building className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-muted-foreground font-medium">My Properties</p>
            <p className="text-2xl font-bold">{stats?.totalProperties}</p>
          </div>
        </div>
        <Link to="/owner/bookings" className="bg-card p-6 rounded-xl border shadow-sm flex items-center gap-4 hover:shadow-md transition-shadow">
          <div className="p-3 bg-blue-500/10 text-blue-500 rounded-lg"><Users className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-muted-foreground font-medium">Active Visits</p>
            <p className="text-2xl font-bold">{stats?.activeVisits}</p>
          </div>
        </Link>
        <div className="bg-card p-6 rounded-xl border shadow-sm flex items-center gap-4">
          <div className="p-3 bg-green-500/10 text-green-500 rounded-lg"><TrendingUp className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-muted-foreground font-medium">Total Revenue</p>
            <p className="text-2xl font-bold">{stats?.totalRevenue}</p>
          </div>
        </div>
        <div className="bg-card p-6 rounded-xl border shadow-sm flex items-center gap-4">
          <div className="p-3 bg-purple-500/10 text-purple-500 rounded-lg"><Calendar className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-muted-foreground font-medium">Total Views</p>
            <p className="text-2xl font-bold">{stats?.totalViews}</p>
          </div>
        </div>
      </div>

      {/* Properties List */}
      <h2 className="text-2xl font-semibold mb-4">My Properties</h2>
      {properties.length === 0 ? (
        <div className="text-center py-12 bg-card rounded-xl border">
          <Building className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-lg font-medium mb-2">No properties yet</h3>
          <p className="text-muted-foreground mb-4">List your first property to start getting bookings.</p>
          <Link to="/owner/properties/new">
            <Button><Plus className="w-4 h-4 mr-2" /> Add Property</Button>
          </Link>
        </div>
      ) : (
        <div className="bg-card border rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-secondary/50 border-b">
                  <th className="p-4 font-medium text-muted-foreground">Property</th>
                  <th className="p-4 font-medium text-muted-foreground">Location</th>
                  <th className="p-4 font-medium text-muted-foreground">Type</th>
                  <th className="p-4 font-medium text-muted-foreground">Status</th>
                  <th className="p-4 font-medium text-muted-foreground">Actions</th>
                </tr>
              </thead>
              <tbody>
                {properties.map(property => (
                  <tr key={property.id} className="border-b hover:bg-muted/30 transition-colors">
                    <td className="p-4 font-medium">{property.name}</td>
                    <td className="p-4">
                      <div className="flex items-center text-muted-foreground text-sm">
                        <MapPin className="w-3.5 h-3.5 mr-1" /> {property.city}
                      </div>
                    </td>
                    <td className="p-4 capitalize text-sm">{property.property_type}</td>
                    <td className="p-4">
                      {property.is_active ? (
                        <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">Active</span>
                      ) : (
                        <span className="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs font-medium">Inactive</span>
                      )}
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">Edit</Button>
                        <Button variant="outline" size="sm">Visits</Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
