import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/services/api';
import { Building2, MapPin, DollarSign, Bed, Info, Upload } from 'lucide-react';

export function AddProperty() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [images, setImages] = useState([]);

  // Minimal form state to not overcomplicate for now
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    property_type: 'pg',
    gender: 'coliving',
    address: '',
    city: '',
    area: '',
    rent_min: '',
    rent_max: '',
    deposit: '',
    total_beds: '',
    available_beds: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e) => {
    setImages(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Create property (JSON)
      const propResponse = await api.post('/properties/create/', formData);
      const propertyId = propResponse.data.id;

      // 2. Upload images if any
      if (images.length > 0) {
        for (const file of images) {
          const imgData = new FormData();
          imgData.append('property', propertyId);
          imgData.append('images', file); 
          await api.post(`/properties/${propertyId}/upload-images/`, imgData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
        }
      }

      navigate('/owner/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to add property.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-card rounded-2xl shadow-sm mt-8 border border-border">
      <h1 className="text-2xl font-bold mb-6 text-foreground">Add New Property</h1>
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Basic Info */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Info className="w-5 h-5 text-primary" />
            Basic Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Property Name</label>
              <input
                required
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
                placeholder="e.g. Sunrise PG"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Property Type</label>
              <select
                name="property_type"
                value={formData.property_type}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              >
                <option value="hostel">Hostel</option>
                <option value="pg">Paying Guest (PG)</option>
                <option value="coliving">Co-Living</option>
                <option value="flat">Flat/Apartment</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Description</label>
              <textarea
                required
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
                placeholder="Describe your property..."
              />
            </div>
          </div>
        </div>

        {/* Location Info */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <MapPin className="w-5 h-5 text-primary" />
            Location
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Full Address</label>
              <textarea
                required
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                rows={2}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">City</label>
              <input
                required
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Area</label>
              <input
                required
                name="area"
                value={formData.area}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
          </div>
        </div>

        {/* Pricing Info */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-primary" />
            Pricing & Details
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Min Rent</label>
              <input
                type="number"
                required
                name="rent_min"
                value={formData.rent_min}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Max Rent</label>
              <input
                type="number"
                required
                name="rent_max"
                value={formData.rent_max}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Deposit</label>
              <input
                type="number"
                required
                name="deposit"
                value={formData.deposit}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Total Beds</label>
              <input
                type="number"
                required
                name="total_beds"
                value={formData.total_beds}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Available Beds</label>
              <input
                type="number"
                required
                name="available_beds"
                value={formData.available_beds}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:outline-none dark:bg-background"
              />
            </div>
          </div>
        </div>

        {/* Images */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Upload className="w-5 h-5 text-primary" />
            Upload Images
          </h2>
          <div className="border-2 border-dashed border-border rounded-xl p-8 text-center cursor-pointer hover:bg-muted/50 transition-colors">
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
              id="image-upload"
            />
            <label htmlFor="image-upload" className="cursor-pointer flex flex-col items-center">
              <Upload className="w-10 h-10 text-muted-foreground mb-4" />
              <span className="text-sm font-medium">Click to upload photos</span>
              <span className="text-xs text-muted-foreground mt-2">JPG, PNG up to 5MB (Multiple allowed)</span>
            </label>
          </div>
          {images.length > 0 && (
            <div className="text-sm text-green-600 font-medium mt-2">
              {images.length} file(s) selected
            </div>
          )}
        </div>

        <div className="pt-6 border-t flex justify-end gap-4">
          <button
            type="button"
            onClick={() => navigate('/owner/dashboard')}
            className="px-6 py-2 border border-input rounded-lg hover:bg-muted transition-colors font-medium"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-medium disabled:opacity-50"
          >
            {loading ? 'Publishing...' : 'Publish Property'}
          </button>
        </div>
      </form>
    </div>
  );
}
