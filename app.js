import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, Text, View, Image, TouchableOpacity, 
  ScrollView, ActivityIndicator, Modal, SafeAreaView, FlatList 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

// --- MOCK DATA & ASSETS ---
// In a real app, this is your [uploaded icon]
const APP_ICON = "https://via.placeholder.com/100/FFD700/000000?text=BuildAI"; 

// --- MOCK AI SERVICES ---
const mockGemini3Estimate = async (photoUri) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        total: "$4,500",
        breakdown: [
          { item: "Demolition & Prep", cost: "$500" },
          { item: "Materials (Tiles, Grout)", cost: "$1,200" },
          { item: "Labor (Installation)", cost: "$2,500" },
          { item: "Waste Disposal", cost: "$300" },
        ]
      });
    }, 3000); // Simulating 3s processing time
  });
};

const mockNanoBananaGen = async (photoUri) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      // Returns a URL to a "renovated" version of the image
      resolve("https://via.placeholder.com/400/4CAF50/FFFFFF?text=Renovated+View"); 
    }, 5000); // Simulating 5s generation time
  });
};

// --- SCREENS ---

// 1. DASHBOARD SCREEN
const Dashboard = ({ navigation }) => {
  const currentJobs = [
    { id: '1', client: 'Smith Residence', type: 'Kitchen Upgrade', status: 'In Progress', price: '$12,000' },
    { id: '2', client: 'Johnson Fencing', type: 'Fence Repair', status: 'Pending', price: '$2,400' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Image source={{ uri: APP_ICON }} style={styles.logo} />
        <Text style={styles.headerTitle}>ContractorPro</Text>
      </View>
      
      <View style={styles.content}>
        <Text style={styles.sectionTitle}>Current Jobs</Text>
        <FlatList
          data={currentJobs}
          keyExtractor={item => item.id}
          renderItem={({ item }) => (
            <View style={styles.jobCard}>
              <View>
                <Text style={styles.jobClient}>{item.client}</Text>
                <Text style={styles.jobType}>{item.type}</Text>
              </View>
              <View style={{ alignItems: 'flex-end' }}>
                <Text style={styles.jobPrice}>{item.price}</Text>
                <Text style={styles.jobStatus}>{item.status}</Text>
              </View>
            </View>
          )}
        />
        
        <TouchableOpacity 
          style={styles.fab} 
          onPress={() => navigation.navigate('Camera')}
        >
          <Ionicons name="camera" size={28} color="#FFF" />
          <Text style={styles.fabText}>New Estimate</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

// 2. CAMERA / INPUT SCREEN (Mocked)
const CameraScreen = ({ navigation }) => {
  // In a real app, use Expo Camera here. We will simulate taking a pic.
  const takePhoto = () => {
    // Simulating a captured photo URI
    const photoUri = "https://via.placeholder.com/400/CCCCCC/000000?text=Original+Site+Photo";
    navigation.navigate('Estimate', { photoUri });
  };

  return (
    <View style={styles.cameraContainer}>
      <Text style={styles.cameraText}>[Camera Viewfinder]</Text>
      <TouchableOpacity style={styles.captureBtn} onPress={takePhoto}>
        <View style={styles.captureBtnInner} />
      </TouchableOpacity>
    </View>
  );
};

// 3. ESTIMATE & VISUALIZATION SCREEN
const EstimateScreen = ({ route, navigation }) => {
  const { photoUri } = route.params;
  const [loading, setLoading] = useState(true);
  const [estimateData, setEstimateData] = useState(null);
  const [renovatedImage, setRenovatedImage] = useState(null);
  const [fullScreenModal, setFullScreenModal] = useState(false);

  useEffect(() => {
    const processJob = async () => {
      // Parallel execution: Get cost from Gemini, Visuals from Nano Banana
      const estimatePromise = mockGemini3Estimate(photoUri);
      const visualPromise = mockNanoBananaGen(photoUri);

      const [estimate, visual] = await Promise.all([estimatePromise, visualPromise]);
      
      setEstimateData(estimate);
      setRenovatedImage(visual);
      setLoading(false);
    };

    processJob();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }}>
        
        {/* IMAGE AREA */}
        <View style={styles.imageContainer}>
          {loading ? (
            <View>
              <Image source={{ uri: photoUri }} style={styles.mainImage} />
              <View style={styles.overlay}>
                <ActivityIndicator size="large" color="#FFD700" />
                <Text style={styles.overlayText}>Gemini 3 Analyzing...</Text>
                <Text style={styles.overlayTextSmall}>Generating Nano Banana Vision...</Text>
              </View>
            </View>
          ) : (
            <TouchableOpacity onPress={() => setFullScreenModal(true)}>
              <Image source={{ uri: renovatedImage }} style={styles.mainImage} />
              <View style={styles.zoomIcon}>
                 <Ionicons name="expand" size={20} color="#FFF" />
              </View>
              <Text style={styles.imageLabel}>Tap to view Full Screen (Renovated)</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* DATA AREA */}
        {!loading && estimateData && (
          <View style={styles.detailsContainer}>
            <Text style={styles.totalPrice}>{estimateData.total}</Text>
            <Text style={styles.estimateLabel}>Estimated Total</Text>
            
            <View style={styles.divider} />
            
            <Text style={styles.sectionTitle}>Cost Breakdown</Text>
            {estimateData.breakdown.map((item, index) => (
              <View key={index} style={styles.row}>
                <Text style={styles.rowItem}>{item.item}</Text>
                <Text style={styles.rowCost}>{item.cost}</Text>
              </View>
            ))}

            <TouchableOpacity style={styles.actionBtn}>
              <Text style={styles.actionBtnText}>Save Estimate</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>

      {/* FULL SCREEN MODAL */}
      <Modal visible={fullScreenModal} transparent={true}>
        <View style={styles.modalContainer}>
          <TouchableOpacity 
            style={styles.closeBtn} 
            onPress={() => setFullScreenModal(false)}
          >
            <Ionicons name="close-circle" size={40} color="#FFF" />
          </TouchableOpacity>
          <Image source={{ uri: renovatedImage }} style={styles.fullScreenImage} resizeMode="contain" />
        </View>
      </Modal>

    </SafeAreaView>
  );
};

// --- APP NAVIGATION WRAPPER (Simplified) ---
// In a real app, use React Navigation. This is a simple state-based switcher for demo purposes.
export default function App() {
  const [currentScreen, setCurrentScreen] = useState('Dashboard');
  const [params, setParams] = useState({});

  const navigate = (screen, data = {}) => {
    setParams(data);
    setCurrentScreen(screen);
  };

  const route = { params };

  return (
    <>
      <StatusBar style="dark" />
      {currentScreen === 'Dashboard' && <Dashboard navigation={{ navigate }} />}
      {currentScreen === 'Camera' && <CameraScreen navigation={{ navigate }} />}
      {currentScreen === 'Estimate' && <EstimateScreen route={route} navigation={{ navigate }} />}
    </>
  );
}

// --- STYLES ---
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5F5F7' },
  header: { padding: 20, paddingTop: 50, flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFF' },
  logo: { width: 40, height: 40, borderRadius: 10, marginRight: 10 },
  headerTitle: { fontSize: 24, fontWeight: 'bold', color: '#333' },
  content: { padding: 20, flex: 1 },
  sectionTitle: { fontSize: 18, fontWeight: '600', marginBottom: 15, color: '#555' },
  
  // Job Card
  jobCard: { backgroundColor: '#FFF', padding: 15, borderRadius: 12, marginBottom: 10, flexDirection: 'row', justifyContent: 'space-between', shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, elevation: 2 },
  jobClient: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  jobType: { color: '#888', marginTop: 4 },
  jobPrice: { fontSize: 16, fontWeight: 'bold', color: '#2E7D32' },
  jobStatus: { fontSize: 12, color: '#FFA000', marginTop: 4, fontWeight: '600' },
  
  // FAB
  fab: { position: 'absolute', bottom: 30, right: 20, backgroundColor: '#000', flexDirection: 'row', alignItems: 'center', paddingVertical: 12, paddingHorizontal: 20, borderRadius: 30, shadowColor: '#000', shadowOpacity: 0.3, shadowRadius: 5 },
  fabText: { color: '#FFF', fontWeight: 'bold', marginLeft: 8 },

  // Camera
  cameraContainer: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center' },
  cameraText: { color: '#666', marginBottom: 20 },
  captureBtn: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#FFF', justifyContent: 'center', alignItems: 'center' },
  captureBtnInner: { width: 70, height: 70, borderRadius: 35, borderWidth: 2, borderColor: '#000' },

  // Estimate Screen
  imageContainer: { width: '100%', height: 300, backgroundColor: '#DDD', position: 'relative' },
  mainImage: { width: '100%', height: '100%' },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', alignItems: 'center' },
  overlayText: { color: '#FFF', marginTop: 10, fontWeight: 'bold', fontSize: 16 },
  overlayTextSmall: { color: '#DDD', marginTop: 5, fontSize: 12 },
  zoomIcon: { position: 'absolute', bottom: 10, right: 10, backgroundColor: 'rgba(0,0,0,0.5)', padding: 5, borderRadius: 5 },
  imageLabel: { position: 'absolute', bottom: 10, left: 10, color: '#FFF', fontSize: 12, fontWeight: '600', textShadowColor: 'rgba(0,0,0,0.8)', textShadowRadius: 2 },
  
  detailsContainer: { padding: 20 },
  totalPrice: { fontSize: 36, fontWeight: 'bold', color: '#333', textAlign: 'center', marginTop: 10 },
  estimateLabel: { textAlign: 'center', color: '#888', fontSize: 14, marginBottom: 20 },
  divider: { height: 1, backgroundColor: '#E0E0E0', marginVertical: 15 },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  rowItem: { fontSize: 16, color: '#555' },
  rowCost: { fontSize: 16, fontWeight: '600', color: '#333' },
  
  actionBtn: { backgroundColor: '#2E7D32', padding: 15, borderRadius: 10, alignItems: 'center', marginTop: 20 },
  actionBtnText: { color: '#FFF', fontWeight: 'bold', fontSize: 16 },

  // Modal
  modalContainer: { flex: 1, backgroundColor: '#000', justifyContent: 'center' },
  closeBtn: { position: 'absolute', top: 50, right: 20, zIndex: 10 },
  fullScreenImage: { width: '100%', height: '100%' },
});
