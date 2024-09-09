import React from 'react'
import Image from 'next/image'

export default function Component() {
  return (
    <div className="relative max-w-4xl mx-auto font-sans">
      {/* Left side explanatory boxes */}
      <div className="absolute left-0 top-0 w-1/3 pr-4 space-y-4 text-sm">
        <div className="bg-gray-100 p-4 mb-4">
          <p><strong>Las actividades facilitadoras</strong> permiten de forma directa que otras actividades contribuyan significativamente a un objetivo medioambiental.</p>
        </div>
        <div className="bg-gray-100 p-4 mb-4">
          <p><strong>Las actividades de transición</strong> son actividades para las que todavía no se dispone de alternativas con bajas emisiones de carbono y que, entre otras cosas, tienen niveles de emisión de gases de efecto invernadero que se corresponden con los mejores resultados.</p>
        </div>
        <div className="bg-gray-100 p-4">
          <p><strong>Las actividades que se ajustan a la taxonomía</strong> se expresan como un porcentaje de:</p>
          <ul className="list-disc pl-5 space-y-2 mt-2">
            <li><strong>El volumen de negocios</strong>, que refleja el porcentaje de ingresos procedentes de actividades ecológicas de las empresas en las que se invierte.</li>
            <li><strong>La inversión en activo fijo</strong> (CapEx), que muestra las inversiones ecológicas realizadas por las empresas en las que se invierte, por ejemplo, para la transición a una economía verde.</li>
            <li><strong>Los gastos de explotación</strong> (OpEx), que reflejan las actividades operativas ecológicas de las empresas en las que se invierte.</li>
          </ul>
        </div>
      </div>

      {/* Main content */}
      <div className="ml-[35%] space-y-6">
        <div className="flex items-start space-x-4">
          <Image src="/logos_icons/icon_q5.png" alt="Question icon" width={40} height={40} className="mt-1" />
          <div>
            <h2 className="text-xl font-bold mb-2">¿En qué medida se ajustaban las inversiones sostenibles con un objetivo medioambiental a la taxonomía de la UE?</h2>
            <p className="text-sm mb-4">
              El Plan de Previsión no tiene establecido un porcentaje mínimo de alineación de las inversiones de este Plan de Previsión a la Taxonomía de la UE. Al no tener establecido un compromiso mínimo de alineamiento, el dato no es auditado y se reporta a efectos informativos. Los siguientes gráficos muestran el alineamiento del Plan de Previsión con la Taxonomía de la UE a lo largo del periodo de referencia.
            </p>
          </div>
        </div>

        <div className="pl-14">
          <div className="flex items-start space-x-2">
            <div className="w-3 h-3 rounded-full bg-gray-400 mt-1.5"></div>
            <div>
              <h3 className="font-bold mb-2">¿Invirtió el producto financiero en actividades relacionadas con el gas fósil o la energía nuclear que cumplían la taxonomía de la UE1?</h3>
              <div className="space-y-2">
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="form-checkbox" />
                  <span>Sí:</span>
                </label>
                <div className="pl-6 space-x-4">
                  <label className="inline-flex items-center">
                    <input type="checkbox" className="form-checkbox" />
                    <span className="ml-2">En el gas fósil</span>
                  </label>
                  <label className="inline-flex items-center">
                    <input type="checkbox" className="form-checkbox" />
                    <span className="ml-2">En la energía nuclear</span>
                  </label>
                </div>
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="form-checkbox" />
                  <span>No</span>
                </label>
              </div>
              <p className="text-xs mt-2 text-gray-600">
                1Las actividades relacionadas con el gas fósil o la energía nuclear solo cumplirán la taxonomía de la UE cuando contribuyan a limitar el cambio climático («mitigación del cambio climático») y no perjudiquen significativamente ningún objetivo de la taxonomía de la UE (véase la nota explicativa en el margen izquierdo). Los criterios completos aplicables a las actividades económicas relacionadas con el gas fósil y la energía nuclear que cumplen la taxonomía de la UE se establecen en el Reglamento Delegado (UE) 2022/1214 de la Comisión.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}