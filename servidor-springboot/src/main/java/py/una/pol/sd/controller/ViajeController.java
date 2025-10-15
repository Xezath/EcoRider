package py.una.pol.sd.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.stream.Collectors;

import py.una.pol.sd.model.Viaje;
import py.una.pol.sd.service.ViajeService;

@RestController
@RequestMapping("/api/viajes")
public class ViajeController {

    @Autowired
    ViajeService service;

    // LISTAR TODOS LOS VIAJES
    // GET /api/viajes/listar
    @GetMapping(value = "/listar", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Viaje>> listar(
        @RequestParam(required = false) String origen,
        @RequestParam(required = false) String destino) {

        List<Viaje> lista = service.listar(); // Listado completo

        // Aplicamos filtros si vienen
        if (origen != null && !origen.isEmpty()) {
            lista = lista.stream().filter(v -> v.getOrigen().equalsIgnoreCase(origen)).collect(Collectors.toList());
        }
        if (destino != null && !destino.isEmpty()) {
            lista = lista.stream().filter(v -> v.getDestino().equalsIgnoreCase(destino)).collect(Collectors.toList());
        }

        // Ordenamos por ID ascendente
        lista.sort((v1, v2) -> v1.getId().compareTo(v2.getId()));

        return new ResponseEntity<>(lista, HttpStatus.OK);
    }

    // CREAR VIAJE
    // POST /api/viajes/crear
    @PostMapping(value = "/crear", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Viaje> crear(@RequestBody Viaje v) {
        Viaje nuevo = service.guardar(v);
        return new ResponseEntity<>(nuevo, HttpStatus.CREATED);
    }

    // ACTUALIZAR VIAJE
    @PutMapping(value = "/actualizar/{id}", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Viaje> actualizar(@PathVariable Long id, @RequestBody Viaje v) {
        Viaje existente = service.obtenerPorId(id);
        if (existente == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        existente.setOrigen(v.getOrigen());
        existente.setDestino(v.getDestino());
        existente.setHora(v.getHora());
        existente.setCupo(v.getCupo());
        Viaje actualizado = service.guardar(existente);
        return new ResponseEntity<>(actualizado, HttpStatus.OK);
    }

    // ELIMINAR VIAJE
    @DeleteMapping("/eliminar/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        Viaje existente = service.obtenerPorId(id);
        if (existente == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        service.eliminar(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Viaje> obtenerPorId(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(v -> new ResponseEntity<>(v, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }


}
