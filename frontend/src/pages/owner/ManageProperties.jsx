import { useState, useEffect } from 'react';
import { api } from '@/services/api';
import { Building2, Edit, Trash2, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

export function ManageProperties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const res = await api.get('/properties/my/');
        setProperties(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProperties();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to deactivate this property?')) {
      try {
        await api.delete(`/properties/${id}/delete/`);
        setProperties(properties.filter(p => p.id !== id));
      } catch (err) {
        console.error(err);
      }
    }
  };

  if (loading) return <div className="p-8 text-center text-muted-foreground">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6 mt-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Properties</h1>
        <Link 
          to="/owner/properties/new" 
          className="bg-primary text-primary-foreground px-4 py-2 rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          + Add New Property
        </Link>
      </div>

      {properties.length === 0 ? (
        <div className="text-center p-12 border-2 border-dashed rounded-xl bg-muted/20">
          <Building2 className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-medium mb-2">No properties yet</h3>
          <p className="text-muted-foreground mb-6">You haven't listed any properties. Start by adding one!</p>
          <Link to="/owner/properties/new" className="text-primary hover:underline font-medium">Add Property</Link>
        </div>
      ) : (
        <div className="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {properties.map(property => (
            <div key={property.id} className="bg-card rounded-xl border shadow-sm overflow-hidden flex flex-col">
              <img 
                src={property.primary_image || 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&q=80&w=800'} 
                alt={property.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4 flex-grow flex flex-col">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold">{property.name}</h3>
                  <span className={`text-xs px-2 py-1 rounded-full ${property.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {property.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex items-center text-muted-foreground text-sm mb-4">
                  <MapPin className="w-4 h-4 mr-1" />
                  {property.area}, {property.city}
                </div>
                
                <div className="mt-auto flex justify-between items-center pt-4 border-t">
                  <span className="font-bold text-primary">₹{property.rent_min}/mo</span>
                  <div className="flex gap-2">
                    <button className="p-2 text-muted-foreground hover:text-primary transition-colors bg-muted rounded-md" title="Edit">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button onClick={() => handleDelete(property.id)} className="p-2 text-muted-foreground hover:text-destructive transition-colors bg-muted rounded-md" title="Deactivate">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
