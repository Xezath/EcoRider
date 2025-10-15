package py.una.pol.sd.controller;

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
import org.springframework.web.bind.annotation.RestController;

import py.una.pol.sd.model.Vehiculo;
import py.una.pol.sd.service.VehiculoService;

@RestController
@RequestMapping("/api/vehiculos")
public class VehiculoController {
    @Autowired
    VehiculoService service;

    // LISTAR TODOS LOS VEHICULOS
    // GET /api/vehiculos/listar
    @GetMapping(value = "/listar", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Vehiculo>> listar() {
        List<Vehiculo> lista = service.listar();
        return new ResponseEntity<>(lista, HttpStatus.OK);
    }
    
    // GET /api/vehiculos/{id} -> obtener vehículo por id
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vehiculo> obtenerPorId(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(v -> new ResponseEntity<>(v, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // POST /api/vehiculos -> crear vehículo
    @PostMapping(value = "/crear",consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vehiculo> crear(@RequestBody Vehiculo v) {
        Vehiculo creado = service.guardar(v);
        return new ResponseEntity<>(creado, HttpStatus.CREATED);
    }

    // PUT /api/vehiculos/{id} -> actualizar (sobrescribe todos los campos)
    @PutMapping(value = "/actualizar/{id}", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vehiculo> actualizar(@PathVariable Long id, @RequestBody Vehiculo v) {
        return service.buscarPorId(id)
                .map(existing -> {
                    existing.setPlaca(v.getPlaca());
                    existing.setModelo(v.getModelo());
                    existing.setCapacidad(v.getCapacidad());
                    existing.setTipo(v.getTipo());
                    Vehiculo updated = service.guardar(existing);
                    return new ResponseEntity<>(updated, HttpStatus.OK);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // DELETE /api/vehiculos/{id}
    @DeleteMapping("/eliminar/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(v -> {
                    service.eliminar(id);
                    return new ResponseEntity<Void>(HttpStatus.NO_CONTENT);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
}
