export default function Component() {
  return (
    <div className="font-sans">
      <div className="bg-[#FFDAB9] p-4 mb-4">
        <h2 className="text-xl font-bold mb-4">¿Este producto financiero tenía un objetivo de inversión sostenible?</h2>
        <div className="flex justify-center space-x-16">
          <div className="flex items-center">
            <span className="flex mr-2">
              <span className="w-2 h-2 rounded-full bg-green-500 mr-0.5"></span>
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
            </span>
            <div className="w-5 h-5 border border-black bg-white mr-2"></div>
            <span>Sí</span>
          </div>
          <div className="flex items-center">
            <span className="flex mr-2">
              <span className="w-2 h-2 rounded-full bg-green-500 mr-0.5"></span>
              <span className="w-2 h-2 rounded-full bg-white border border-black"></span>
            </span>
            <div className="w-5 h-5 border border-black bg-white mr-2 flex items-center justify-center">
              <span className="font-bold">X</span>
            </div>
            <span>No</span>
          </div>
        </div>
      </div>
      <div className="bg-[#FFE4B5] p-4">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="flex items-start mb-2">
              <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
              <span><strong>Realizó inversiones sostenibles con un objetivo medioambiental:</strong></span>
            </div>
            <div className="ml-7 mb-2">
              <div className="flex items-start">
                <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
                <span>en actividades económicas que se consideran medioambientalmente sostenibles con arreglo a la taxonomía de la UE</span>
              </div>
            </div>
            <div className="ml-7 mb-2">
              <div className="flex items-start">
                <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
                <span>en actividades económicas que no se consideran medioambientalmente sostenibles con arreglo a la taxonomía de la UE</span>
              </div>
            </div>
            <div className="flex items-start mb-2">
              <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
              <span><strong>Realizó inversiones sostenibles con un objetivo social:</strong></span>
            </div>
          </div>
          <div>
            <div className="flex items-start mb-2">
              <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0 flex items-center justify-center">
                <span className="font-bold">X</span>
              </div>
              <span><strong>Promovió características medioambientales o sociales</strong> y, aunque no tenía como objetivo una inversión sostenible, tuvo un porcentaje del 4,12% de inversiones sostenibles</span>
            </div>
            <div className="ml-7 mb-2">
              <div className="flex items-start">
                <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
                <span>con un objetivo medioambiental en actividades económicas que se consideran medioambientalmente sostenibles con arreglo a la taxonomía de la UE</span>
              </div>
            </div>
            <div className="ml-7 mb-2">
              <div className="flex items-start">
                <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0 flex items-center justify-center">
                  <span className="font-bold">X</span>
                </div>
                <span>con un objetivo medioambiental en actividades económicas que no se consideran medioambientalmente sostenibles con arreglo a la taxonomía de la UE</span>
              </div>
            </div>
            <div className="ml-7 mb-2">
              <div className="flex items-start">
                <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0 flex items-center justify-center">
                  <span className="font-bold">X</span>
                </div>
                <span>con un objetivo social</span>
              </div>
            </div>
            <div className="flex items-start mb-2">
              <div className="w-5 h-5 border border-black bg-white mr-2 mt-0.5 flex-shrink-0"></div>
              <span><strong>Promovió características medioambientales o sociales</strong>, pero no realizó ninguna inversión sostenible</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}