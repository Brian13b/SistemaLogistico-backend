

function Seguimiento({ darkMode }) {
    return (
      <div>
        <h1 className="text-2xl font-bold mb-6">Seguimiento de Vehículos</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="md:col-span-2">
            <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} h-96 flex items-center justify-center`}>
              <div className="text-center">
                <p className={`text-xl ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Mapa de Seguimiento</p>
                <p className={`${darkMode ? 'text-gray-500' : 'text-gray-400'} mt-2`}>Aquí se mostraría el mapa con la ubicación de los vehículos</p>
              </div>
            </div>
          </div>
          
          <div>
            <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} h-96 overflow-auto`}>
              <h2 className="text-lg font-semibold mb-4">Vehículos Activos</h2>
              <div className="space-y-4">
                <div className={`p-3 rounded ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} flex items-center space-x-3`}>
                  <div className={`w-3 h-3 rounded-full bg-green-500`}></div>
                  <div>
                    <p className="font-medium">AB123CD</p>
                    <p className="text-sm">Córdoba - En ruta</p>
                  </div>
                </div>
                <div className={`p-3 rounded ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} flex items-center space-x-3`}>
                  <div className={`w-3 h-3 rounded-full bg-green-500`}></div>
                  <div>
                    <p className="font-medium">EF456GH</p>
                    <p className="text-sm">Mendoza - En ruta</p>
                  </div>
                </div>
                <div className={`p-3 rounded ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} flex items-center space-x-3`}>
                  <div className={`w-3 h-3 rounded-full bg-yellow-500`}></div>
                  <div>
                    <p className="font-medium">XY789ZW</p>
                    <p className="text-sm">Buenos Aires - Detenido</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

export default Seguimiento;