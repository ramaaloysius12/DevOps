import math

class GeofencingVerifier:
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Menghitung jarak antara dua titik koordinat dalam satuan meter menggunakan Haversine Formula.
        """
        R = 6371000  # Radius bumi dalam meter
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat2) - float(lat1))
        delta_lambda = math.radians(float(lon2) - float(lon1))

        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def verify_presence(user_lat, user_long, office_lat=-6.2088, office_long=106.8456, max_radius_meters=50.0):
        """
        Memvalidasi jika karyawan berada di dalam radius yang diizinkan (default 50 meter).
        """
        distance = GeofencingVerifier.calculate_distance(user_lat, user_long, office_lat, office_long)
        return distance <= max_radius_meters, distance