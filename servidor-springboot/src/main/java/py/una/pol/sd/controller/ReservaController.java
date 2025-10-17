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

import py.una.pol.sd.model.Reserva;
import py.una.pol.sd.service.ReservaService;

@RestController
@RequestMapping("/api/reservas")
public class ReservaController {

    @Autowired
    ReservaService service;

    // GET /api/reservas/listar -> listar todas las reservas
    @GetMapping(value = "/listar", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Reserva>> listar() {
        List<Reserva> lista = service.listar();
        return new ResponseEntity<>(lista, HttpStatus.OK);
    }

    // GET /api/reservas/{id} -> obtener reserva por id
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Reserva> obtenerPorId(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(r -> new ResponseEntity<>(r, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // POST /api/reservas/crear -> crear reserva
    @PostMapping(value = "/crear", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Reserva> crear(@RequestBody Reserva r) {
        Reserva nueva = service.guardar(r);
        return new ResponseEntity<>(nueva, HttpStatus.CREATED);
    }

    // PUT /api/reservas/actualizar/{id} -> actualizar reserva
    @PutMapping(value = "/actualizar/{id}", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Reserva> actualizar(@PathVariable Long id, @RequestBody Reserva r) {
        return service.buscarPorId(id)
                .map(existing -> {
                    existing.setUsuarioId(r.getUsuarioId());
                    existing.setViajeId(r.getViajeId());
                    existing.setEstado(r.getEstado());
                    existing.setFechaReserva(r.getFechaReserva());
                    Reserva updated = service.guardar(existing);
                    return new ResponseEntity<>(updated, HttpStatus.OK);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // DELETE /api/reservas/eliminar/{id} -> eliminar reserva
    @DeleteMapping("/eliminar/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(r -> {
                    service.eliminar(id);
                    return new ResponseEntity<Void>(HttpStatus.NO_CONTENT);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
}