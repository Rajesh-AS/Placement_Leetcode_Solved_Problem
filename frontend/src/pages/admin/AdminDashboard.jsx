import { useState, useEffect } from 'react';
import { adminService } from '@/services/adminService';
import { api } from '@/services/api';
import { Users, Building2, Calendar, Star, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/common/Button';

export function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [properties, setProperties] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statsRes = await adminService.getDashboardStats();
        setStats(statsRes);
        
        // Fetch unverified properties
        const propRes = await api.get('/properties/admin/all/?is_verified=false');
        setProperties(propRes.data.results || propRes.data || []);

        // Fetch recent users
        const usersRes = await api.get('/auth/admin/users/');
        setUsers(usersRes.data.results || usersRes.data || []);
      } catch (err) {
        console.error('Failed to fetch admin data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handlePropertyAction = async (id, action) => {
    try {
      await api.post(`/properties/admin/${id}/action/`, { action });
      setProperties(properties.filter(p => p.id !== id));
      alert(`Property ${action}ed successfully.`);
    } catch (err) {
      alert('Failed to perform action.');
    }
  };

  const handleUserAction = async (id, action) => {
    try {
      await api.post(`/auth/admin/users/${id}/action/`, { action });
      setUsers(users.map(u => u.id === id ? { ...u, is_active: action !== 'suspend' } : u));
    } catch (err) {
      alert('Failed to perform action.');
    }
  };

  if (loading) {
    return <div className="p-8"><div className="shimmer h-64 rounded-2xl w-full" /></div>;
  }

  const displayStats = stats || {
    total_users: users.length || 0,
    total_properties: properties.length || 0,
    total_bookings: 0,
    total_reviews: 0,
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[var(--foreground)]">Admin Dashboard</h1>
        <p className="text-[var(--muted-foreground)] mt-1">Platform overview and management</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        {[
          { label: 'Total Users', value: displayStats.total_users, icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
          { label: 'Properties Listed', value: displayStats.total_properties, icon: Building2, color: 'text-[var(--primary)]', bg: 'bg-[var(--primary)]/10' },
          { label: 'Total Bookings', value: displayStats.total_bookings, icon: Calendar, color: 'text-[var(--gold)]', bg: 'bg-[var(--gold)]/10' },
          { label: 'Reviews Posted', value: displayStats.total_reviews, icon: Star, color: 'text-purple-600', bg: 'bg-purple-100' },
        ].map((stat, i) => (
          <div key={i} className="bg-[var(--card)] border border-[var(--border)] p-6 rounded-2xl flex items-center gap-4 hover:shadow-md transition-shadow">
            <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${stat.bg}`}>
              <stat.icon className={`w-7 h-7 ${stat.color}`} />
            </div>
            <div>
              <p className="text-sm font-medium text-[var(--muted-foreground)]">{stat.label}</p>
              <h3 className="text-2xl font-bold text-[var(--foreground)]">{stat.value.toLocaleString()}</h3>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Properties to Verify */}
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl overflow-hidden">
          <div className="p-5 border-b border-[var(--border)] flex justify-between items-center">
            <h3 className="font-bold text-lg text-[var(--foreground)]">Pending Verifications</h3>
          </div>
          <div className="p-0 overflow-x-auto">
            {properties.length === 0 ? (
              <div className="text-center py-10 text-[var(--muted-foreground)] text-sm">
                No pending properties to verify at the moment.
              </div>
            ) : (
              <table className="w-full text-left text-sm">
                <thead className="bg-[var(--secondary)]">
                  <tr>
                    <th className="p-4 font-medium">Property</th>
                    <th className="p-4 font-medium">Owner</th>
                    <th className="p-4 font-medium text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {properties.map(prop => (
                    <tr key={prop.id} className="hover:bg-[var(--secondary)]/50 transition-colors">
                      <td className="p-4 font-semibold">{prop.name}</td>
                      <td className="p-4">{prop.owner?.first_name || 'Owner'}</td>
                      <td className="p-4 flex gap-2 justify-end">
                        <Button size="sm" onClick={() => handlePropertyAction(prop.id, 'verify')} className="bg-green-600 hover:bg-green-700">Verify</Button>
                        <Button size="sm" variant="outline" onClick={() => handlePropertyAction(prop.id, 'reject')} className="text-red-600 hover:text-red-700">Reject</Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Recent Users */}
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl overflow-hidden">
          <div className="p-5 border-b border-[var(--border)] flex justify-between items-center">
            <h3 className="font-bold text-lg text-[var(--foreground)]">Recent Users</h3>
          </div>
          <div className="p-0 overflow-x-auto">
            {users.length === 0 ? (
              <div className="text-center py-10 text-[var(--muted-foreground)] text-sm">
                No recent users.
              </div>
            ) : (
              <table className="w-full text-left text-sm">
                <thead className="bg-[var(--secondary)]">
                  <tr>
                    <th className="p-4 font-medium">Name</th>
                    <th className="p-4 font-medium">Role</th>
                    <th className="p-4 font-medium">Status</th>
                    <th className="p-4 font-medium text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border)]">
                  {users.map(user => (
                    <tr key={user.id} className="hover:bg-[var(--secondary)]/50 transition-colors">
                      <td className="p-4 font-semibold">{user.first_name} {user.last_name}</td>
                      <td className="p-4 capitalize">{user.role}</td>
                      <td className="p-4">
                        {user.is_active ? 
                          <span className="text-green-600 flex items-center gap-1"><CheckCircle className="w-3 h-3" /> Active</span> :
                          <span className="text-red-600 flex items-center gap-1"><XCircle className="w-3 h-3" /> Suspended</span>
                        }
                      </td>
                      <td className="p-4 flex justify-end">
                        {user.is_active ? (
                          <Button size="sm" variant="outline" onClick={() => handleUserAction(user.id, 'suspend')} className="text-red-600 hover:text-red-700">Suspend</Button>
                        ) : (
                          <Button size="sm" variant="outline" onClick={() => handleUserAction(user.id, 'activate')} className="text-green-600 hover:text-green-700">Activate</Button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
